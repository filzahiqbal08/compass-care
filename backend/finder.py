"""
Compass Care back end: the Python version of the Excel Top_5_Nearest tab.

This module does exactly what Location_Test / Top_5_Nearest do in
compass_care_milestone1.xlsx:

  1. Look up the center point of the ZIP the user typed.
  2. Check the ZIP is inside San Diego County.
  3. Keep sites that match the chosen site group, service and language.
  4. Measure the straight-line distance from the ZIP's center to each
     matching site.
  5. Return the 5 closest.
  6. If fewer than 5 match, fill the rest with the nearest Health
     center sites, labeled as a fallback.

Read find_nearest() first; everything else supports it.
"""

import math
import sqlite3
from dataclasses import dataclass

DB_PATH = "compass_care.db"
EARTH_RADIUS_MILES = 3958.8  # same assumption as Location_Test!$E$3 in Excel


def haversine_miles(lat1, lon1, lat2, lon2):
    """Straight-line distance in miles between two points on Earth.

    Same formula as the Location_Test / Calc_Top5 tabs in Excel.
    """
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    a = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return EARTH_RADIUS_MILES * 2 * math.asin(math.sqrt(a))


@dataclass
class Site:
    site_key: str
    name: str
    site_group: str
    address: str
    city: str
    zip5: str
    phone: str
    services: str
    organization: str
    languages: str
    language_confidence: str
    insurance_note: str
    insurance_confidence: str
    lat: float
    lon: float
    distance_miles: float = None   # rounded, for display
    _sort_distance: float = None   # unrounded, for ordering only
    result_type: str = "Match"  # "Match" or "Fallback"


def _row_to_site(row):
    return Site(
        site_key=row["site_key"], name=row["name"], site_group=row["site_group"],
        address=row["address"], city=row["city"], zip5=row["zip5"], phone=row["phone"],
        services=row["services"] or "", organization=row["organization"] or "",
        languages=row["languages"] or "", language_confidence=row["language_confidence"] or "",
        insurance_note=row["insurance_note"] or "", insurance_confidence=row["insurance_confidence"] or "",
        lat=row["lat"], lon=row["lon"],
    )


def _site_group_matches(site_group, chosen_group):
    """Same rule as Top_5_Nearest!$C$5 in Excel."""
    if chosen_group == "All":
        return True
    if chosen_group == "Public sites":
        return site_group not in ("School", "Other")
    return site_group == chosen_group


def _service_matches(services_text, chosen_service):
    """Same rule as the Service filter in Excel (a plain substring search)."""
    if chosen_service == "Any":
        return True
    return chosen_service.lower() in services_text.lower()


def _language_matches(languages_text, chosen_language):
    """Same rule as the Language filter in Excel: an exact language match,
    or an 'interpreter services' statement, counts as a match."""
    if chosen_language == "Any":
        return True
    t = languages_text.lower()
    return chosen_language.lower() in t or "interpret" in t


def get_zip_info(conn, zip5):
    """Look up a ZIP's center point and county.

    Returns None if the ZIP is not in the list at all (Excel's
    "ZIP not found in the list" case).
    """
    row = conn.execute(
        "SELECT zip, city, county, lat, lon FROM zip_centroids WHERE zip = ?",
        (zip5,),
    ).fetchone()
    return dict(row) if row else None


def find_nearest(conn, zip5, site_group="Public sites", service="Any", language="Any", limit=5):
    """The Python equivalent of the Top_5_Nearest tab.

    Returns a dict shaped like one row of the Excel workbook's
    Answer_Key tab:
        {
          "zip": "92105",
          "status": "OK" | "ZIP not found in the list" | "Outside San Diego County: out of scope",
          "matches": 22,          # sites that matched the filters, before the fallback
          "message": "",          # the note Excel writes in column D10, or "" if none
          "results": [Site, ...], # up to `limit` results, matches first, fallback after
        }
    """
    zip_info = get_zip_info(conn, zip5)
    if zip_info is None:
        return {"zip": zip5, "status": "ZIP not found in the list", "matches": 0, "message": "", "results": []}
    if zip_info["county"] != "San Diego County":
        return {"zip": zip5, "status": "Outside San Diego County: out of scope", "matches": 0, "message": "", "results": []}

    center_lat, center_lon = zip_info["lat"], zip_info["lon"]

    rows = conn.execute("SELECT * FROM sites").fetchall()
    matches = []
    for row in rows:
        if not _site_group_matches(row["site_group"], site_group):
            continue
        if not _service_matches(row["services"] or "", service):
            continue
        if not _language_matches(row["languages"] or "", language):
            continue
        site = _row_to_site(row)
        d = haversine_miles(center_lat, center_lon, site.lat, site.lon)
        site._sort_distance = d
        site.distance_miles = round(d, 1)
        matches.append(site)
    matches.sort(key=lambda s: s._sort_distance)

    match_count = len(matches)
    results = matches[:limit]

    message = ""
    if match_count < limit:
        # Fallback: nearest Health center sites not already in the results.
        used_keys = {s.site_key for s in results}
        fallback_candidates = []
        for row in rows:
            if row["site_group"] != "Health center" or row["site_key"] in used_keys:
                continue
            site = _row_to_site(row)
            d = haversine_miles(center_lat, center_lon, site.lat, site.lon)
            site._sort_distance = d
            site.distance_miles = round(d, 1)
            site.result_type = "Fallback"
            fallback_candidates.append(site)
        fallback_candidates.sort(key=lambda s: s._sort_distance)
        results = results + fallback_candidates[: limit - match_count]

        if match_count == 0:
            message = "No sites match these filters. Showing the nearest health centers instead; call to ask."
        else:
            message = f"Only {match_count} site(s) match. The rest are the nearest health centers; call to ask."

    return {
        "zip": zip5,
        "status": "OK",
        "matches": match_count,
        "message": message,
        "results": results,
    }


def connect(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == "__main__":
    # Quick manual check: same as typing 92105 / Public sites / Dental / Any
    # into Top_5_Nearest.
    conn = connect()
    result = find_nearest(conn, "92105", "Public sites", "Dental", "Any")
    print(f"ZIP {result['zip']}: {result['status']}, {result['matches']} match(es)")
    for s in result["results"]:
        print(f"  {s.distance_miles:>5} mi  {s.result_type:<8} {s.name}")
    conn.close()
