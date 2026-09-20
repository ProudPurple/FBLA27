# Nonprofit Volunteer Managment

Your solution should help nonprofit organizations coordinate volunteers, manage service opportunities, maintain records, and monitor participation while supporting the needs of both volunteers and organization leaders.

## TODO
- Capable of scraping more sites
- Send out info
- Better UI
- Record Keeping

You only need to touch two folders:
- `frontend/src/` — the React UI
- `backend/app/` — the Python backend (API, database, scraper)

## 1. Prerequisites

- **Node.js** (LTS) — https://nodejs.org — installs `node` and `npm`
- **Python 3.11+** — https://www.python.org/downloads/ — on Windows, check
  "Add python.exe to PATH" during install
- **Git** — https://git-scm.com

Check they're installed by running in a terminal:
```powershell
node --version
python --version
git --version
```
If any of those error, that tool isn't installed / isn't on PATH yet.

## 2. Get the code

```powershell
git clone <https://github.com/ProudPurple/FBLA27>
cd FBLA27
```

## 3. First-time Setup

**Frontend:**
```powershell
cd frontend
npm install
cd ..
```

**Backend:**
```powershell
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python -m playwright install chromium
cd ..
```
May take a minute to download

## 4. Add the SignUpGenius sheets to track

Open `backend/app/config.py` and add your sheet URL(s):
```python
SIGNUP_GENIUS_URLS: list[str] = [
    "https://www.signupgenius.com/go/XXXXXXXXXXXX",
]
```
Save the file. This list starts empty — nothing shows up in the app until
you add at least one URL here.

## 5. Run it (every time you work on it)

Two terminals, both from the project root (`FBLA27/`):

**Terminal 1:**
```powershell
cd frontend
npm run dev
```
Leave this running — it's the live dev server for the UI.

**Terminal 2:**
```powershell
cd backend
.venv\Scripts\python run.py --dev
```
This opens the actual app window. `--dev` points it at the dev server from
Terminal 1 and turns on devtools (right-click inside the window → Inspect).

To see your changes:
- **Frontend edits** (anything in `frontend/src/`) — hot-reload automatically,
  just save the file.
- **Backend edits** (anything in `backend/app/`) — stop Terminal 2
  (`Ctrl+C`) and rerun `.venv\Scripts\python run.py --dev`.
- If routing/navigation starts acting weird after an edit (stale page state),
  close and reopen the app window rather than trying to hot-reload past it.

Click **Refresh** inside the app to scrape the URLs from `config.py` and
pull the latest sign-up counts into the local database.

## 6. Common problems

- **Window opens blank / errors about the bridge** — make sure Terminal 1
  (`npm run dev`) is actually running before you start Terminal 2.
- **Refresh times out or errors** — SignUpGenius pages keep background
  requests going, so the scraper waits for the page to load rather than for
  the network to go fully idle. If a specific sheet still fails, the page
  layout for that sheet may not match what `backend/app/scraper.py` expects.
- **Data looks wrong / missing after a database change** — this project
  doesn't have migrations set up yet. If someone changes the database models
  in `backend/app/db.py`, delete the old database file and let it recreate
  itself:
  ```powershell
  Remove-Item "$env:LOCALAPPDATA\SignUpGeniusTracker\app.db"
  ```
  (You'll lose whatever was scraped before — hit Refresh again after.)

## 7. Building a standalone .exe (optional — only needed to hand someone a
single file that runs without installing Node/Python)

```powershell
cd frontend
npm run build

cd ../backend
.venv\Scripts\pyinstaller build.spec
```
The .exe lands at `backend/dist/SignUpGeniusTracker.exe`. Whoever runs it
still needs Chromium installed via `playwright install chromium` once on
their machine — PyInstaller doesn't bundle it.

## Project layout

```
frontend/
  src/                    <- the React app (this is what you'll edit)
    App.tsx                routes: "/" -> EventList, "/event/:id" -> Event
    pages/EventList.tsx     home page: list of tracked sign-up sheets
    pages/Event.tsx          detail page: one sheet's slot breakdown
    lib/pywebview.ts          typed wrapper around window.pywebview.api

backend/
  app/                    <- the Python backend (this is what you'll edit)
    main.py                 opens the app window
    api.py                   methods callable from the frontend
    db.py                    database tables (SQLAlchemy)
    scraper.py                Playwright scraping logic
    scheduler.py               background auto-refresh timer
    config.py                   <- put your SignUpGenius URLs here
    paths.py                     where the database file lives
  run.py                  entry point used to start the app
  build.spec              PyInstaller packaging config
  requirements.txt        Python dependencies
```
