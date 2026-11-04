# Compass Care

A clinic finder for immigrants in San Diego County. Type a ZIP code, pick the service, site type and clinic language you need, and see the nearest matching clinics (5 by default, or 10, 15, or all). A "Book appointment" button opens a second page with the clinic's phone number.

## How it was built

1. **Milestone 1: Excel** (`milestone-1/compass_care_milestone1.xlsx`). Filtered the national HRSA site list to San Diego County, deduplicated it to 731 sites, grouped and tagged them, and built the Top 5 Nearest lookup. The `Answer_Key` tab holds 14 hand-checked test cases.
2. **Milestone 2: Python backend** (`backend/`). `finder.py` reproduces the Excel logic against a SQLite database (`compass_care.db`). Passes all 14 Answer_Key cases (`test_finder.py`). `api.py` exposes the same logic as a FastAPI service (`test_api.py`); optional, kept for future hosting.
3. **Milestone 3: Streamlit app** (`app/`). Calls `backend/finder.py` directly. Page 1 = search + result cards; page 2 = booking/phone page. Language picker is built in; translations are loaded from `app/translations.json` (languages without translations show "soon").
4. **Next:** translations (Python NLLB model, Gemini as backup), cosmetics pass, then hosting (Oracle Cloud).

`frontend/` is the earlier plain-HTML front end, superseded by the Streamlit app.
A diagram of the data flow is in `diagrams/system-diagram.html` (open it in a browser).

## Folder map

```
app/              Streamlit app (Home.py, search_page.py, book_page.py, i18n.py, strings.py, common.py)
.streamlit/       theme and settings
backend/          finder.py, api.py, compass_care.db, tests
data/raw/         original HRSA export, never edited (checksum included)
data/processed/   San Diego County subset
milestone-1/      the Excel workbook (logic design + tests)
frontend/         old HTML front end (superseded)
diagrams/         system diagram
requirements.txt  what the Streamlit app needs
```

## Run the app locally

From the top folder of the project, in Terminal:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/Home.py
```
It opens at http://localhost:8501. (If it asks for an email, just press Enter.) Stop it with Control+C.

## Run the tests

```
cd backend
pip install -r requirements.txt     # only needed for the API tests
python3 test_finder.py              # logic vs. Excel Answer_Key (14 cases)
```

## Adding a language

Translations live in `app/translations.json`:
`{ "es": { "ui": {...same keys as strings.py...}, "services": {...}, "data": {...} } }`.
A language code that is not in the file shows as "(soon)" in the picker and displays English.

## Data note

`data/raw/SITE_DASHBOARD.csv` is the unmodified HRSA export (129,141 rows). Verify it with `shasum -a 256 -c SITE_DASHBOARD.csv.sha256` from inside `data/raw/`.
