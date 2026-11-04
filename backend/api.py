"""
Compass Care API: the web "front door" for finder.py.

This file adds no new logic of its own. It takes a web request like

    GET /sites?zip=92105&site_group=Public+sites&service=Dental&language=Spanish

reads those four values, calls find_nearest() in finder.py (the exact
same function the Excel tests were checked against), and sends back
what it returns as JSON, the plain structured format a web page reads.

Run it locally with:
    uvicorn api:app --reload

Then open:
    http://127.0.0.1:8000/docs
for the interactive test page FastAPI builds automatically -- try a
search there before any front end exists.
"""

from typing import Literal

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from finder import connect, find_nearest

app = FastAPI(
    title="Compass Care API",
    description="Looks up the nearest San Diego County clinics for a ZIP code, "
                 "site group, service and language. A thin wrapper around finder.py.",
    version="1.0.0",
)

# Lets the front end (served from a different local address/port, or later
# a real website) call this API from the browser. Without this, the
# browser blocks the request even though the server itself is fine.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite connections can't be shared across threads, and FastAPI runs each
# request's function in its own worker thread. So instead of one shared
# connection, each request opens a quick new one and closes it when done.
# compass_care.db is small and read-only here, so this has no real cost.

SITE_GROUPS = Literal["Public sites", "All", "Health center", "Hospital", "Referral-only", "School", "Other"]


class SiteResult(BaseModel):
    """One clinic result, shaped for the front end's result cards."""
    site_key: str
    name: str
    site_group: str
    address: str
    city: str
    zip5: str
    phone: str
    services: list[str]
    organization: str
    languages: str
    language_confidence: str
    insurance_note: str
    insurance_confidence: str
    lat: float
    lon: float
    distance_miles: float
    result_type: Literal["Match", "Fallback"]


class SearchResponse(BaseModel):
    """The whole answer for one search -- one row of the Excel Answer_Key tab."""
    zip: str
    status: Literal["OK", "ZIP not found in the list", "Outside San Diego County: out of scope"]
    matches: int
    message: str
    results: list[SiteResult]


def _to_site_result(site) -> SiteResult:
    services = [s for s in site.services.split("; ") if s] if site.services else []
    return SiteResult(
        site_key=site.site_key, name=site.name, site_group=site.site_group,
        address=site.address, city=site.city, zip5=site.zip5, phone=site.phone,
        services=services, organization=site.organization,
        languages=site.languages, language_confidence=site.language_confidence,
        insurance_note=site.insurance_note, insurance_confidence=site.insurance_confidence,
        lat=site.lat, lon=site.lon,
        distance_miles=site.distance_miles, result_type=site.result_type,
    )


@app.get("/sites", response_model=SearchResponse)
def get_sites(
    zip: str = Query(..., min_length=5, max_length=5, pattern=r"^\d{5}$",
                      description="A 5-digit ZIP code, e.g. 92105"),
    site_group: SITE_GROUPS = Query("Public sites", description="Which kind of site to include"),
    service: str = Query("Any", description="A service name (e.g. Dental), or Any"),
    language: str = Query("Any", description="A language name (e.g. Spanish), or Any"),
):
    """Find the 5 nearest matching sites for a ZIP code.

    Same inputs and same logic as the Top_5_Nearest tab in the Excel
    workbook: this endpoint calls find_nearest() and returns exactly
    what it computes, just as JSON instead of spreadsheet cells.
    """
    conn = connect()
    try:
        result = find_nearest(conn, zip, site_group=site_group, service=service, language=language)
    finally:
        conn.close()
    return SearchResponse(
        zip=result["zip"],
        status=result["status"],
        matches=result["matches"],
        message=result["message"],
        results=[_to_site_result(s) for s in result["results"]],
    )


@app.get("/health")
def health():
    """A quick check that the API is running and can reach the database."""
    conn = connect()
    try:
        count = conn.execute("SELECT COUNT(*) FROM sites").fetchone()[0]
    finally:
        conn.close()
    return {"status": "ok", "sites_in_database": count}
