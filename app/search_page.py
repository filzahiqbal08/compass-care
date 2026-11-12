"""Page 1: search for clinics and see the nearest results."""

import streamlit as st

from common import display_name, find_nearest, list_all, load_options, md_safe, new_connection, public_site_count
from i18n import apply_direction, language_picker, t, t_data, t_service
from style import apply_style, brand

# value sent to the search engine -> text key
SITE_GROUPS = {
    "Public sites": "site_public",
    "All": "site_all",
    "Health center": "site_health_center",
    "Hospital": "site_hospital",
    "Referral-only": "site_referral",
    "School": "site_school",
}
COUNTS = ["5", "10", "15", "all"]

STATUS_MESSAGES = {
    "Invalid ZIP": "msg_invalid_zip",
    "ZIP not found in the list": "msg_zip_not_found",
    "Outside San Diego County: out of scope": "msg_outside_county",
}

# Quick-pick tiles: service name in the data -> icon
TILES = [
    ("Primary care", ":material/stethoscope:", "primary"),
    ("Dental", ":material/dentistry:", "dental"),
    ("Behavioral health", ":material/psychology:", "behavioral"),
    ("Pediatrics", ":material/child_care:", "pediatrics"),
    ("Women's health", ":material/pregnant_woman:", "womens"),
    ("Vision", ":material/visibility:", "vision"),
]


def trust_badge(confidence):
    if confidence == "High":
        return f":green-badge[:material/verified: {t('badge_checked')}]"
    if confidence in ("Medium", "Low"):
        return f":orange-badge[:material/call: {t('badge_confirm')}]"
    return ""


def result_card(site, position):
    fallback = site.result_type == "Fallback"
    with st.container(key=f"cc_box_card_{position}"):
        st.html('<span class="cc-result"></span>')
        left, right = st.columns([3, 1.35], vertical_alignment="top")
        with left:
            sub = f'<p class="cc-sub">{_html(site.organization)}</p>' if site.organization else ""
            st.html(f'<p class="cc-name">{_html(display_name(site.name))}</p>{sub}')
            st.markdown(f":material/location_on: {md_safe(site.address)}, {md_safe(site.city)} {site.zip5}")
            services = [s.strip() for s in (site.services or "").split(";") if s.strip()]
            if services:
                st.markdown(" ".join(f":blue-badge[{md_safe(t_service(s.split('(')[0].strip()))}]" for s in services))
            languages = t_data(site.languages) if site.languages else t("not_listed")
            insurance = t_data(site.insurance_note) if site.insurance_note else t("not_listed")
            st.html(f'<p class="cc-note"><b>{_html(t("languages_label"))}:</b> {_html(languages)}</p>'
                    f'<p class="cc-note"><b>{_html(t("insurance_label"))}:</b> {_html(insurance)}</p>')
            badges = " ".join(b for b in (trust_badge(site.language_confidence or site.insurance_confidence),) if b)
            if fallback:
                badges = f":orange-badge[:material/info: {t('fallback_tag')}] " + badges
            if badges.strip():
                st.markdown(badges)
        with right:
            if site.distance_miles is not None:
                st.markdown(f"**:material/near_me: {t('miles_away', miles=f'{site.distance_miles:.1f}')}**")
            phone = site.phone or t("phone_not_listed")
            st.html(f'<p class="cc-line">{_html(phone)}</p>')
            if st.button(t("book_button"), icon=":material/event_available:",
                         key=f"book_{position}_{site.site_key}", type="primary", use_container_width=True):
                st.session_state["selected_site"] = {
                    "name": display_name(site.name), "address": site.address, "city": site.city, "zip5": site.zip5,
                    "phone": site.phone, "languages": site.languages, "insurance_note": site.insurance_note,
                }
                st.switch_page("book_page.py")


def _html(text):
    """Escape text going into hand-written HTML."""
    return (str(text or "")).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pick(options, value, default=0):
    return options.index(value) if value in options else default


# ---------------------------------------------------------------- page
apply_style()
top = st.columns([3, 2], vertical_alignment="center")
with top[1]:
    language_picker("search")          # first, so the rest uses the chosen language
apply_direction()
with top[0]:
    brand(t("app_title"))

services, clinic_languages = load_options()
saved = st.session_state.get("search", {})
service_options = ["Any"] + services
language_options = ["Any"] + clinic_languages
group_options = list(SITE_GROUPS)


for key, default in (("f_zip", saved.get("zip", "")), ("f_service", saved.get("service", "Any")),
                     ("f_group", saved.get("group", "Public sites")),
                     ("f_language", saved.get("language", "Any")), ("f_browse", saved.get("browse", False))):
    st.session_state.setdefault(key, default)


def run_search(service=None):
    """Remember what was asked. Used by the Search button and the quick-pick tiles."""
    if service is not None:
        st.session_state["f_service"] = service
    st.session_state["search"] = {
        "zip": st.session_state.get("f_zip", "").strip(),
        "service": st.session_state.get("f_service", "Any"),
        "group": st.session_state.get("f_group", "Public sites"),
        "language": st.session_state.get("f_language", "Any"),
        "browse": st.session_state.get("f_browse", False),
    }


with st.container(key="cc_hero"):
    st.html(f'<div class="cc-hero-title">{_html(t("hero_title"))}</div>'
            f'<div class="cc-hero-sub">{_html(t("hero_sub"))}</div>')

    with st.container(key="cc_box_search"):
        row = st.columns([2, 3, 1.6], vertical_alignment="bottom")
        row[0].text_input(
            t("zip_label"), max_chars=5,
            placeholder=t("zip_placeholder"), key="f_zip", on_change=run_search,
        )
        row[1].selectbox(
            t("service_label"), service_options,
            format_func=lambda v: t("service_any") if v == "Any" else t_service(v), key="f_service",
        )
        row[2].button(t("search_button"), icon=":material/search:", type="primary",
                      use_container_width=True, on_click=run_search)

        with st.expander(t("more_filters"), icon=":material/tune:"):
            more = st.columns(2)
            more[0].selectbox(
                t("site_type_label"), group_options,
                format_func=lambda v: t(SITE_GROUPS[v]), key="f_group",
            )
            more[1].selectbox(
                t("clinic_language_label"), language_options,
                format_func=lambda v: t("clinic_language_any") if v == "Any" else v, key="f_language",
            )
            st.toggle(t("browse_toggle"), key="f_browse")

    st.html('<div class="cc-trust">'
            f'<span>✔ {_html(t("trust_free"))}</span>'
            f'<span>✔ {_html(t("trust_private"))}</span>'
            f'<span>✔ {_html(t("trust_sites", n=public_site_count()))}</span></div>')


st.markdown(f"**{t('quick_title')}**")
with st.container(key="cc_tiles"):
    available = [tile for tile in TILES if tile[0] in services]
    for col, (name, icon, tid) in zip(st.columns(len(available)), available):
        col.button(f"{icon} {t_service(name)}", key=f"tile_{tid}",
                   use_container_width=True, on_click=run_search, args=(name,))

params = st.session_state.get("search")
if not params:
    st.info(t("start_prompt"), icon=":material/pin_drop:")
else:
    st.divider()
    browse = params.get("browse", False)
    if browse:
        # Every matching clinic in the county, A to Z. The ZIP code is not used.
        conn = new_connection()
        try:
            result = list_all(conn, site_group=params["group"], service=params["service"],
                              language=params["language"])
        finally:
            conn.close()
    else:
        # Quick toggle: changing it re-shows results instantly, no new search.
        count = st.segmented_control(
            t("count_label"), COUNTS, default="5", key="count",
            format_func=lambda v: t("count_all") if v == "all" else v,
        ) or "5"
        conn = new_connection()
        try:
            result = find_nearest(
                conn, params["zip"], site_group=params["group"], service=params["service"],
                language=params["language"], limit=None if count == "all" else int(count),
            )
        finally:
            conn.close()

    if result["status"] != "OK":
        st.error(t(STATUS_MESSAGES.get(result["status"], "msg_zip_not_found")), icon=":material/error:")
    else:
        if result["message"]:
            key = {0: "msg_fallback_none", 1: "msg_fallback_one"}.get(result["matches"], "msg_fallback_some")
            st.warning(t(key, n=result["matches"]), icon=":material/info:")
        results = result["results"]
        if not results:
            st.info(t("msg_no_results"))
        else:
            summary = (t("browse_summary", matches=result["matches"]) if browse else
                       t("results_summary", shown=len(results), matches=result["matches"], zip=params["zip"]))
            st.markdown(f"**{summary}**")
            for position, site in enumerate(results):
                result_card(site, position)

st.caption(t("footer"))
