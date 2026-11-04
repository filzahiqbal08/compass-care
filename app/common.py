"""Shared pieces: the connection to the search engine in backend/finder.py."""

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from finder import connect, find_nearest, list_all  # noqa: E402  (needs the path above)

DB_PATH = str(BACKEND / "compass_care.db")

# Languages that can appear in the clinic data. Only the ones that actually
# show up in the database are offered in the dropdown.
CLINIC_LANGUAGE_CANDIDATES = [
    "Spanish", "Chinese", "Mandarin", "Cantonese", "Vietnamese", "Tagalog", "Korean",
    "Farsi", "Persian", "Russian", "Punjabi", "Arabic", "Hindi", "Somali", "Kurdish",
    "Taiwanese", "Italian", "Gujarati", "Lao", "French", "Hmong", "Sign language",
]


def new_connection():
    """A fresh database connection. SQLite connections can't be shared between
    Streamlit's threads, so every search opens its own (it's tiny and fast)."""
    return connect(DB_PATH)


# Listed in the data, but not somewhere a patient can go for care.
NOT_FOR_PATIENTS = {
    "Administrative office", "Correctional facility", "Organ procurement",
    "Health workforce training", "Temporary COVID site",
}


@st.cache_data
def load_options():
    """Service and clinic-language choices, read from the database itself."""
    conn = new_connection()
    try:
        services = set()
        for (text,) in conn.execute("SELECT services FROM sites"):
            for part in (text or "").split(";"):
                base = part.split("(")[0].strip()   # "Vision (optometry)" -> "Vision"
                if base and base not in NOT_FOR_PATIENTS:
                    services.add(base)
        language_text = " ".join(
            text for (text,) in conn.execute("SELECT languages FROM sites WHERE languages IS NOT NULL")
        ).lower()
    finally:
        conn.close()
    languages = [name for name in CLINIC_LANGUAGE_CANDIDATES if name.lower() in language_text]
    return sorted(services, key=str.lower), languages


def md_safe(text):
    """Stop '$' in clinic names or notes from being read as math by Streamlit."""
    return (text or "").replace("$", "\\$")
