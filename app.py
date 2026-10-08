"""Local educational prototype. Run: python app.py"""
import argparse
import csv
import hashlib
import hmac
import io
import json
import os
from pathlib import Path
import secrets
import threading
import time
import webbrowser
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from src.storage import Store
from src.service import Monitor
from src.telemetry import SCENARIOS, sample

ROOT = Path(__file__).resolve().parent

def make_server(port=8000, db_path=None, password=None):
    monitor = Monitor(Store(db_path or ROOT / 'data' / 'monitoring.sqlite3'))
    actual_password = password or os.environ.get('CAPSTONE_PASSWORD') or secrets.token_urlsafe(12)
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac('sha256', actual_password.encode(), salt, 120000)
    sessions = {}
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def reply(self, code, payload, kind='application/json', cookie=None):
            if isinstance(payload, (dict, list)):
                payload = json.dumps(payload)
            encoded = payload.encode('utf-8')
            self.send_response(code)
            self.send_header('Content-Type', kind + '; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('Referrer-Policy', 'no-referrer')
            if cookie:
                self.send_header('Set-Cookie', cookie)
            self.end_headers()
            self.wfile.write(encoded)

        def session(self):
            cookies = SimpleCookie()
            try:
                cookies.load(self.headers.get('Cookie', ''))
                token = cookies['session'].value if 'session' in cookies else ''
            except Exception:
                return None
            with lock:
                session = sessions.get(token)
                if session and session['expires'] > time.time():
                    return dict(session, token=token)
                sessions.pop(token, None)
            return None

        def do_GET(self):
            if self.path == '/':
                return self.reply(200, (ROOT / 'src' / 'dashboard.html').read_text(), 'text/html')
            session = self.session()
            if not session:
                return self.reply(401, {'error': 'Administrator login required.'})
            if self.path == '/api/state':
                return self.reply(200, {'records': monitor.store.list(), 'rules': monitor.rules,
                    'scenarios': {k: v[0] for k, v in SCENARIOS.items()}, 'csrf': session['csrf']})
            if self.path == '/api/report':
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(['id', 'timestamp', 'scenario', 'priority', 'incident_detected', 'rule', 'evidence'])
                for row in monitor.store.list():
                    writer.writerow([row['id'], row['timestamp'], row['scenario'], row['priority'],
                        row['incident_detected'], row['rule'], '; '.join(row['evidence'])])
                return self.reply(200, output.getvalue(), 'text/csv')
            return self.reply(404, {'error': 'Unknown route.'})

        def do_POST(self):
            # Reject cross-origin requests. Browser requests must use this exact local host.
            origin = self.headers.get('Origin')
            if origin and origin != f'http://{self.headers.get("Host")}':
                return self.reply(403, {'error': 'Origin rejected.'})
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 16384:
                    raise ValueError('Invalid request size.')
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError('Request must be an object.')
            except (ValueError, UnicodeDecodeError):
                return self.reply(400, {'error': 'Invalid JSON request.'})
            if self.path == '/api/login':
                entered = data.get('password', '')
                if not isinstance(entered, str) or len(entered) > 200:
                    return self.reply(401, {'error': 'Incorrect credentials.'})
                entered_digest = hashlib.pbkdf2_hmac('sha256', entered.encode(), salt, 120000)
                if data.get('username') != 'admin' or not hmac.compare_digest(entered_digest, digest):
                    return self.reply(401, {'error': 'Incorrect credentials.'})
                token = secrets.token_urlsafe(32)
                with lock:
                    sessions[token] = {'csrf': secrets.token_urlsafe(32), 'expires': time.time() + 1800}
                return self.reply(200, {'ok': True}, cookie=f'session={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=1800')
            session = self.session()
            if not session:
                return self.reply(401, {'error': 'Administrator login required.'})
            if not hmac.compare_digest(self.headers.get('X-CSRF-Token', ''), session['csrf']):
                return self.reply(403, {'error': 'Request token missing or invalid.'})
            if self.path == '/api/logout':
                with lock:
                    sessions.pop(session['token'], None)
                return self.reply(200, {'ok': True}, cookie='session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0')
            if self.path == '/api/process':
                try:
                    scenario = data.get('scenario')
                    if scenario == 'custom':
                        telemetry = data.get('telemetry')
                    elif scenario in SCENARIOS:
                        telemetry = sample(scenario)
                    else:
                        raise ValueError('Select a known synthetic scenario.')
                    return self.reply(200, monitor.process(telemetry))
                except (ValueError, TypeError, KeyError) as exc:
                    return self.reply(400, {'error': str(exc)})
            return self.reply(404, {'error': 'Unknown route.'})

        def log_message(self, fmt, *args):
            # Log status and path, never request bodies, cookies, or credentials.
            print(f'{self.address_string()} {fmt % args}')

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    return server, actual_password

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Local synthetic cloud monitoring demo')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    try:
        server, password = make_server(args.port)
    except OSError as exc:
        raise SystemExit(f'Could not start: {exc}. Try: python app.py --port 8001')
    print(f'Open http://127.0.0.1:{args.port}\nUsername: admin\nTemporary password: {password}')
    print('Synthetic local prototype. Do not expose publicly. Stop with Ctrl+C.')
    if not args.no_browser:
        webbrowser.open(f'http://127.0.0.1:{args.port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
