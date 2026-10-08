import copy
import json
from pathlib import Path
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
import http.cookiejar
from app import make_server
from src.telemetry import sample, validate
from src.rules import detect_and_classify, load_rules
from src.storage import Store
from src.service import Monitor

class RuleTests(unittest.TestCase):
    def classify(self, t):
        return detect_and_classify(validate(t), load_rules())

    def test_five_scenarios(self):
        for scenario, expected in [('normal','Normal'),('low','Low'),('medium','Medium'),('high','High'),('outage','High')]:
            with self.subTest(scenario=scenario):
                r=self.classify(sample(scenario))
                self.assertEqual(r['priority'], expected)
                self.assertEqual(r['incident_detected'], expected!='Normal')

    def test_outage_overrides_low_cpu(self):
        self.assertEqual(self.classify(sample('outage'))['rule'], 'H1 Service unavailable')

    def test_high_requires_all_three_contextual_conditions(self):
        for field, value in [('cpu_percent',30),('response_ms',180),('application_errors',0)]:
            t=sample('high');t[field]=value
            self.assertNotEqual(self.classify(t)['priority'],'High')

    def test_threshold_boundary(self):
        t=sample('normal');t['cpu_percent']=84.99
        self.assertEqual(self.classify(t)['priority'],'Normal')
        t['cpu_percent']=85
        self.assertEqual(self.classify(t)['priority'],'Low')

    def test_evidence_tracks_actual_conditions(self):
        r=self.classify(sample('high'))
        self.assertEqual(len(r['evidence']),4)
        self.assertTrue(any('1500' in e for e in r['evidence']))

    def test_invalid_data_rejected(self):
        for field, value in [('cpu_percent',101),('memory_percent',float('nan')),
                ('disk_percent',True),('service_available','false'),('response_ms',-1),
                ('application_errors',1.5),('timestamp','2026-09-30')]:
            with self.subTest(field=field):
                t=sample('normal');t[field]=value
                with self.assertRaises(ValueError):validate(t)

    def test_unknown_sensitive_fields_discarded(self):
        t=sample('normal');t['password']='not-for-storage'
        self.assertNotIn('password',validate(t))

    def test_sqlite_persistence_and_rejected_record(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'test.db';m=Monitor(Store(path));m.process(sample('high'))
            bad=sample('normal');bad['cpu_percent']=-1
            with self.assertRaises(ValueError):m.process(bad)
            records=Store(path).list()
            self.assertEqual(len(records),1)
            self.assertEqual(records[0]['priority'],'High')
            self.assertEqual(records[0]['telemetry']['application_errors'],5)

class ServerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.server,_=make_server(0,Path(self.temp.name)/'test.db','test-password')
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.base=f'http://127.0.0.1:{self.server.server_port}'
        self.client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join();self.temp.cleanup()

    def request(self,path,body=None,csrf=None):
        headers={}
        if body is not None:headers['Content-Type']='application/json'
        if csrf:headers['X-CSRF-Token']=csrf
        req=urllib.request.Request(self.base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
        return self.client.open(req)

    def login(self):
        self.request('/api/login',{'username':'admin','password':'test-password'})
        return json.load(self.request('/api/state'))['csrf']

    def test_unauthenticated_data_and_report_denied(self):
        for route in ['/api/state','/api/report']:
            with self.assertRaises(urllib.error.HTTPError) as e:self.request(route)
            self.assertEqual(e.exception.code,401)

    def test_wrong_password_denied(self):
        with self.assertRaises(urllib.error.HTTPError) as e:self.request('/api/login',{'username':'admin','password':'wrong'})
        self.assertEqual(e.exception.code,401)

    def test_csrf_required(self):
        self.login()
        with self.assertRaises(urllib.error.HTTPError) as e:self.request('/api/process',{'scenario':'high'})
        self.assertEqual(e.exception.code,403)

    def test_processing_state_export_and_logout(self):
        token=self.login()
        r=json.load(self.request('/api/process',{'scenario':'high'},token))
        self.assertEqual(r['priority'],'High')
        state=json.load(self.request('/api/state'))
        self.assertEqual(state['records'][0]['id'],r['id'])
        self.assertIn('H2 High CPU',self.request('/api/report').read().decode())
        self.request('/api/logout',{},token)
        with self.assertRaises(urllib.error.HTTPError) as e:self.request('/api/state')
        self.assertEqual(e.exception.code,401)

if __name__=='__main__':unittest.main()
