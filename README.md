# Compass Care

A clinic finder for immigrants in San Diego County. Type a ZIP code, pick the kind of site, service and language you need, and get the 5 nearest matching clinics, with a fallback to nearby health centers when too few match.

## How it was built

1. **Milestone 1: Excel** (`milestone-1/compass_care_milestone1.xlsx`). Filtered the national HRSA site list to San Diego County, deduplicated it to 731 sites, grouped and tagged them, and built the Top 5 Nearest lookup. The `Answer_Key` tab holds 14 hand-checked test cases.
2. **Milestone 2: Python backend** (`backend/`). `finder.py` reproduces the Excel logic against a SQLite database (`compass_care.db`). `api.py` exposes it as `GET /sites` with FastAPI. Both pass all 14 Answer_Key cases (`test_finder.py`, `test_api.py`).
3. **Milestone 3: front end** (`frontend/`). Plain HTML, CSS and JavaScript that call the API and show results as cards.
4. **Next:** host backend and front end publicly (Oracle Cloud).

A diagram of the whole data flow is in `diagrams/system-diagram.html` (open it in a browser).

## Folder map

```
data/raw/         original HRSA export, never edited (checksum included)
data/processed/   San Diego County subset
milestone-1/      the Excel workbook (logic design + tests)
backend/          finder.py, api.py, compass_care.db, tests, requirements.txt
frontend/         index.html, style.css, app.js
diagrams/         system diagram
```

## Run it locally

You need two Terminal windows.

**Window 1: the API**
```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --reload
```
The API runs at http://127.0.0.1:8000 (interactive test page at /docs).

**Window 2: the front end**
```
cd frontend
python3 -m http.server 5500
```
Open http://127.0.0.1:5500 in a browser.

## Run the tests

With the API running in Window 1, open a third Terminal window:
```
cd backend
source venv/bin/activate
python3 test_finder.py     # logic vs. Excel Answer_Key
python3 test_api.py        # same 14 cases over HTTP (API must be on port 8008 for this script; edit BASE_URL if using 8000)
```

## Data note

`data/raw/SITE_DASHBOARD.csv` is the unmodified HRSA export (129,141 rows). Verify it with `shasum -a 256 -c SITE_DASHBOARD.csv.sha256` from inside `data/raw/`.
