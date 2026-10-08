# Run the prototype and prepare your video

## 1 Download and extract

Download `Unit_4_Monitoring_Prototype_Fe.zip` to your computer. Extract it.
Open the `capstone_prototype` folder inside. Do not run files while they are
still inside the ZIP. The folder contains `app.py`, `src`, `config`, and `docs`.

## 2 Check Python

On Mac, open Terminal and type:

```sh
python3 --version
```

On Windows, open Command Prompt and type:

```bat
py --version
```

Use Python 3.10 or newer. If Python is missing, install it from
https://www.python.org/downloads/ and reopen the terminal. On Windows, enable
the installer option to add Python to PATH if offered.

## 3 Open the project

In your editor (for example, VS Code), use Open Folder and select
`capstone_prototype`. Open its integrated terminal. It must be in the folder
containing `app.py`. Alternatively type `cd ` in a terminal, followed by the
quoted path to that folder. The terminal path should end in `capstone_prototype`.

## 4 Create a virtual environment

Mac/Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
python --version
```

Windows Command Prompt (not PowerShell):

```bat
py -m venv .venv
.venv\Scripts\activate.bat
python --version
```

No pip installation is needed. `requirements.txt` documents that there are no
third-party dependencies. SQLite comes with the Python environment used here.
In VS Code, select the `.venv` Python interpreter if the editor asks.

If you are in PowerShell, avoid activation-policy changes by using:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe app.py
```

## 5 Run the tests

In the activated terminal:

```sh
python -m unittest discover -s tests -v
```

Expect 12 tests and `OK`. Tests use temporary databases and do not add demo
observations to your dashboard.

## 6 Start the application

```sh
python app.py
```

Leave this terminal running. Open http://127.0.0.1:8000 if the browser does not
open automatically. Log in as `admin` with the temporary password printed in
the terminal. Copy it before recording. Restarting changes the password.
Stop the application with Ctrl+C when finished.

If port 8000 is busy, use `python app.py --port 8001`, then open
http://127.0.0.1:8001. If the browser says connection refused, confirm the server
is still running. If Python says it cannot find `app.py`, correct your current folder.

## 7 Practice the demonstration

Select each scenario and click **Process telemetry**:

| Scenario | Expected result |
| --- | --- |
| Normal operation | Normal, no incident detected |
| Isolated CPU increase | Low |
| CPU and memory pressure | Medium |
| CPU with slow service and errors | High |
| Service unavailable | High, even with normal CPU |

Inspect input/output JSON. Filter saved results by High. Download the CSV.
Refresh the page and verify results remain. Sign out to show the login boundary.
The SQLite file is created automatically at `data/monitoring.sqlite3`.

Optional validation demo: after running a case, expand custom JSON, change
`cpu_percent` to `101`, and click **Process custom input**. It must reject the
observation without increasing the saved count. Restore a valid sample before
continuing.

For an empty recording database, stop the application and rename its generated
SQLite file as a backup. Restart to create a fresh database. Never delete your
only useful records. Keep generated data and `.venv` out of GitHub.

## 8 Record in ScreenPal

Follow the assigned ScreenPal tutorial. Use screen, webcam, and microphone.
Test that your ID is readable for 5–10 seconds. After ID verification, put the
ID away and continue the same recording with your screen demonstration.
Aim for 6–7 minutes. Use `RECORDING_SCRIPT.md` as speaking notes.

Show the environment, real processing, reporting, and architecture. Do not
substitute screenshots for running the app. Do not claim live cloud collection,
sustained monitoring, validated accuracy, or a functioning CI/CD pipeline.

## 9 Review and submit

Play the recording and check ID clarity, readable screen text, audible narration,
both working features, all four prompt aspects, and duration. Submit through
the course's required method. If a link is required, verify instructor access.

The ZIP itself is a working aid; the assignment submission is your recorded video.

## 10 Add to your existing repository

After local verification, copy these source files into a new development branch
of your existing project. Keep your prior design documents and repository history.
Review collisions before replacing files. This package contains no Git history
and has not been pushed to your GitHub repository.
