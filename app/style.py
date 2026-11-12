"""Look and feel: one stylesheet for every page.

Colors come from .streamlit/config.toml; this file only adds what the theme
can't do (rounded cards, tile buttons, spacing). Edit values here to restyle.
"""

import streamlit as st

CSS = """
<style>
:root{--navy:#1d2a6e;--blue:#1f6fd0;--sky:#e8f1fd;--ink:#1c2a4a;--muted:#5a6a88;--line:#dbe4f3;--green:#1e9e63}

/* page width and breathing room */
[data-testid="stMainBlockContainer"]{max-width:880px;padding-top:4.6rem;padding-bottom:3rem}
/* Streamlit's own top bar (Fork / GitHub on the live site): match the page color */
[data-testid="stHeader"]{background:#f3f7fd}
h1,h2,h3,h5{letter-spacing:-0.01em;color:var(--navy)}

/* logo + name */
.cc-brand{display:flex;align-items:center;gap:.6rem;font-size:1.6rem;font-weight:800;color:var(--navy);letter-spacing:-.02em}
.cc-brand b{color:var(--blue);font-weight:800}
.cc-brand img{width:2.3rem;height:2.3rem;flex:none}

/* hero band behind the search */
.st-key-cc_hero{background:linear-gradient(135deg,#1d2a6e 0%,#2448b4 60%,#2f7be0 100%);
  border-radius:22px;padding:1.5rem 1.5rem 1.2rem;margin-bottom:1.2rem}
.cc-hero-title{font-size:2.05rem;line-height:1.2;font-weight:800;color:#fff;margin:.1rem 0 .3rem}
.cc-hero-sub{color:#d6e4ff;font-size:1.05rem;margin-bottom:.9rem}
.cc-trust{display:flex;flex-wrap:wrap;gap:.5rem 1.4rem;color:#e6eeff;font-size:.93rem;margin:.9rem 0 0}
.cc-trust span{display:inline-flex;align-items:center;gap:.35rem}

/* every box = a soft white card (boxes are named cc_box_* in the code) */
[class*="st-key-cc_box"]{background:#fff;border:1px solid var(--line)!important;border-radius:16px;padding:1rem 1.1rem;gap:.55rem}
[class*="st-key-cc_box_card"]:hover{box-shadow:0 6px 20px rgba(29,42,110,.13)}

/* input boxes inside the search card: light outline so they stand out */
.st-key-cc_box_search{background:#f6f9fe!important}
.st-key-cc_box_search [data-testid="stTextInputRootElement"],
.st-key-cc_box_search [data-testid="stSelectbox"] div:has(> div > input[role="combobox"]),
.st-key-cc_box_search [data-testid="stSelectbox"] div[class*="e1oobldh0"]{border:1px solid #c5d3ea!important;border-radius:10px}

/* big rounded buttons */
.stButton>button,.stFormSubmitButton>button,[data-testid="stLinkButton"] a{border-radius:12px;font-weight:600}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{min-height:2.9rem}

/* quick-pick tiles: each icon has its own color */
.st-key-cc_tiles .stButton>button{min-height:4.2rem;border-radius:14px;background:#fff;border:1px solid var(--line);color:var(--navy)}
.st-key-cc_tiles .stButton>button p{font-size:1.02rem;font-weight:700}
.st-key-cc_tiles .stButton>button:hover{border-color:var(--blue);background:var(--sky)}
.st-key-tile_primary span[role="img"]{color:#1f6fd0!important}
.st-key-tile_dental span[role="img"]{color:#0e9fb3!important}
.st-key-tile_behavioral span[role="img"]{color:#7a4fd1!important}
.st-key-tile_pediatrics span[role="img"]{color:#e8871e!important}
.st-key-tile_womens span[role="img"]{color:#d6457f!important}
.st-key-tile_vision span[role="img"]{color:#1e9e63!important}

/* tiles: a wrapping grid, 3 per row (2 on phones) */
.st-key-cc_tiles [data-testid="stHorizontalBlock"]{flex-wrap:wrap}
.st-key-cc_tiles [data-testid="stColumn"]{min-width:calc(33.333% - .67rem)!important;flex:0 0 calc(33.333% - .67rem)!important}
.st-key-cc_tiles .stButton>button{height:auto;padding:.7rem .5rem}
.st-key-cc_tiles .stButton>button *{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;max-width:none!important;text-align:center}
@media (max-width:640px){
  .st-key-cc_tiles [data-testid="stColumn"]{min-width:calc(50% - .5rem)!important;flex:0 0 calc(50% - .5rem)!important}
  .st-key-cc_tiles .stButton>button p{font-size:.95rem}
}

/* result card text */
.cc-name{font-size:1.2rem;font-weight:700;color:var(--blue);line-height:1.3;margin:0 0 .15rem}
.cc-sub{color:var(--muted);font-size:.92rem;margin:.1rem 0 .4rem}
.cc-line{color:var(--ink);font-size:.95rem;margin:.15rem 0}
.cc-note{color:var(--muted);font-size:.88rem;margin:.1rem 0}

@media (max-width:640px){
  [data-testid="stMainBlockContainer"]{padding-left:1rem;padding-right:1rem}
  .cc-hero-title{font-size:1.6rem}
  .st-key-cc_hero{padding:1.1rem 1rem}
}
</style>
"""


def apply_style():
    st.html(CSS)


LOGO = (
    '<img alt="" src="data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgNDAgNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiByeD0iMTEiIGZpbGw9IiMxZjZmZDAiLz48cGF0aCBkPSJNMjAgNi41IDIzLjYgMTYuNCAzMy41IDIwIDIzLjYgMjMuNiAyMCAzMy41IDE2LjQgMjMuNiA2LjUgMjAgMTYuNCAxNi40WiIgZmlsbD0iI2ZmZiIvPjxjaXJjbGUgY3g9IjIwIiBjeT0iMjAiIHI9IjIuNiIgZmlsbD0iIzFmNmZkMCIvPjwvc3ZnPg==">'
)


def brand(title):
    """Logo (a compass star) and name, shown at the top left of every page."""
    first, _, rest = title.partition(" ")
    name = f"{first} <b>{rest}</b>" if rest else first
    st.html(f'<div class="cc-brand">{LOGO}<span>{name}</span></div>')
