"""The language switch.

English text lives in strings.py. Every other language is read from
translations.json, which looks like this:

    {
      "es": {
        "ui":       {"search_button": "Buscar", ...},   # same keys as strings.py
        "services": {"Dental": "Dental", ...},           # service names
        "data":     {"<English clinic note>": "<translation>", ...}
      },
      ...
    }

A language that isn't in translations.json yet shows English, with a short
"coming soon" note, so nothing is ever blank or half-translated.
"""

import json
from pathlib import Path

import streamlit as st

from strings import EN

# code: (the language's own name, text direction)
LANGUAGES = {
    "en": ("English", "ltr"),
    "es": ("Español", "ltr"),
    "zh-Hans": ("中文 (简体)", "ltr"),
    "zh-Hant": ("中文 (繁體)", "ltr"),
    "vi": ("Tiếng Việt", "ltr"),
    "tl": ("Tagalog", "ltr"),
    "ko": ("한국어", "ltr"),
    "fa": ("فارسی", "rtl"),
    "ru": ("Русский", "ltr"),
    "pa": ("ਪੰਜਾਬੀ", "ltr"),
    "ar": ("العربية", "rtl"),
    "hi": ("हिन्दी", "ltr"),
}

_FILE = Path(__file__).with_name("translations.json")


@st.cache_data
def _load():
    try:
        return json.loads(_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def current_lang():
    return st.session_state.get("_lang", "en")


def language_ready(code):
    return code == "en" or code in _load()


def t(key, **values):
    """Text for `key` in the chosen language (English if there is no translation)."""
    text = _load().get(current_lang(), {}).get("ui", {}).get(key) or EN[key]
    return text.format(**values) if values else text


def t_service(name):
    return _load().get(current_lang(), {}).get("services", {}).get(name, name)


def t_data(text):
    """Translate a clinic note (languages / insurance text) if we have it."""
    return _load().get(current_lang(), {}).get("data", {}).get(text, text)


def language_picker(where):
    """The language dropdown. Call it first on each page, before any t() text."""
    codes = list(LANGUAGES)

    def label(code):
        name = LANGUAGES[code][0]
        return name if language_ready(code) else f"{name} (soon)"

    choice = st.selectbox(
        ":material/translate: Language",
        codes,
        index=codes.index(current_lang()),
        format_func=label,
        key=f"lang_picker_{where}",
    )
    st.session_state["_lang"] = choice
    if not language_ready(choice):
        st.caption(EN["translation_coming"])


def apply_direction():
    """Right-to-left layout for Arabic and Persian."""
    if LANGUAGES[current_lang()][1] == "rtl":
        st.markdown(
            "<style>[data-testid='stMainBlockContainer']{direction:rtl;text-align:right}</style>",
            unsafe_allow_html=True,
        )
