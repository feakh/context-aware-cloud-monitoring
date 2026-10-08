# Context Aware Cloud Monitoring

Initial Python prototype for Fechukwu Akhmedzhanov's MSIT capstone.

**Start with `docs/START_HERE.md`, then rehearse using `docs/RECORDING_SCRIPT.md`.**

This version runs locally with Python 3.10 or newer and no third-party packages.
It provides administrator login, synthetic telemetry validation, transparent
contextual classification, SQLite storage, a browser dashboard, priority filtering,
and CSV reporting. It does not collect live cloud data or perform remediation.

## Quick start

From this folder, run `python3 app.py` on Mac/Linux or `py app.py` on Windows.
The browser opens automatically. Username: `admin`. Copy the temporary password
printed in the terminal. It changes when the application restarts.

## Structure

| File | Responsibility |
| --- | --- |
| `app.py` | Local HTTP routes, administrator session, orchestration |
| `src/telemetry.py` | Synthetic observations, validation, field minimization |
| `src/rules.py` | Contextual conditions, detection, classification, evidence |
| `src/service.py` | Connect validation, rules, and storage |
| `src/storage.py` | SQLite persistence |
| `src/dashboard.html` | Login, scenario controls, results, filtering, export |
| `config/rules.json` | Prototype thresholds |
| `tests/test_monitoring.py` | Rule, persistence, and HTTP integration tests |

Run tests: `python3 -m unittest discover -s tests -v` (Windows: replace `python3` with `py`).

## Scope and limitations

- Generated data only. Five monitored categories: CPU, memory, disk, service
  availability/response time, and application error events represented by a count.
- Rules classify each observation. No historical time-window correlation or
  sustained-condition detection is implemented yet.
- Thresholds are illustrative choices, not production SLAs or validated findings.
- SQLite retains saved observations; UI and CSV show the most recent 200.
- Single administrator role, 30-minute sessions, process-local session storage.
- Password is generated at startup or supplied through `CAPSTONE_PASSWORD`.
  No password is stored in source or SQLite. Keep the terminal password out of
  the published recording when possible.
- Local loopback HTTP only. No TLS, account provisioning, login rate limiting,
  production deployment, or automated remediation. Do not expose this server
  on a public network.
- Tests demonstrate specific cases. No measured detection rate, false-positive
  rate, latency benchmark, or accuracy claim is made.
- No CI/CD workflow is included or claimed as operational. It remains proposed
  work in the Unit 4 reflection.

## Relationship to the written reflection

The reflection describes proposed CI/CD practices. This package implements the
initial application, not that pipeline. Its current tests use Python's built-in
`unittest`; pytest remains an optional future tool. The initial application now
goes beyond design/repository preparation. Before submitting the reflection,
replace its final status sentence with:

> These CI/CD practices are proposed; the initial prototype now supports synthetic telemetry processing and incident reporting, while the automated pipeline remains to be implemented.

Review, run, and understand the code before presenting it. Follow the course's
requirements for acknowledging assistance. Do not describe features as your
completed implementation until you have run and verified them.

## Technical documentation

Python Software Foundation. (n.d.). *venv—Creation of virtual environments*.
https://docs.python.org/3/library/venv.html

Python Software Foundation. (n.d.). *http.server—HTTP servers*.
https://docs.python.org/3/library/http.server.html

Python Software Foundation. (n.d.). *sqlite3—DB-API 2.0 interface for SQLite databases*.
https://docs.python.org/3/library/sqlite3.html
