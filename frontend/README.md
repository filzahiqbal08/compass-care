# Compass Care — Front End

This is the real front end: an actual web page that calls your live API
and shows real results. It's three plain files — `index.html`,
`style.css`, `app.js` — no build step, no framework, no install needed.

## Run it locally (2 terminal windows)

**Window 1 — start the API** (same as before):
```
cd /path/to/compass-care/backend
source venv/bin/activate
uvicorn api:app --reload
```
This runs at `http://127.0.0.1:8000` by default.

**Window 2 — start the front end:**
```
cd /path/to/compass-care/frontend
python3 -m http.server 5500
```
Then open your browser to:
```
http://127.0.0.1:5500
```

You should see the search form. Type in a ZIP code and hit Search — it
calls the API in Window 1 and shows the real results.

## If it says it can't reach the server

1. Confirm Window 1 is still running and didn't crash.
2. Open `app.js` and check the first line after the comments:
   ```
   const API_BASE_URL = "http://127.0.0.1:8000";
   ```
   This must match wherever `uvicorn` printed that it's running. If you
   started it with `--port 8008` instead, change this to `8008`.

## For your dad / hosting on Oracle

This folder (`frontend/`) is a complete static site — any web host can
serve `index.html`, `style.css`, and `app.js` as-is. The only thing that
changes when it moves off your laptop is `API_BASE_URL` in `app.js`:
right now it points at your local machine; once the backend (`backend/`
folder — api.py, finder.py, compass_care.db) is deployed somewhere with
a real address, that line just needs to point there instead. Everything
else — the page, the styling, the search logic — works unchanged.
