"""Page 1: search for clinics and see the nearest results."""

import streamlit as st

from common import find_nearest, list_all, load_options, md_safe, new_connection
from i18n import apply_direction, language_picker, t, t_data, t_service
from strings import EN

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


def result_card(site, position):
    fallback = site.result_type == "Fallback"
    with st.container(border=True):
        st.markdown(f"##### {md_safe(site.name)}")
        if site.distance_miles is not None:
            meta = f":material/near_me: {t('miles_away', miles=f'{site.distance_miles:.1f}')}"
            if fallback:
                meta += f" &nbsp; :orange-badge[:material/info: {t('fallback_tag')}]"
            st.markdown(meta)

        st.markdown(f":material/location_on: {md_safe(site.address)}, {md_safe(site.city)} {site.zip5}")
        phone = site.phone or t("phone_not_listed")
        st.markdown(f":material/call: {phone}")

        services = [s.strip() for s in (site.services or "").split(";") if s.strip()]
        if services:
            st.markdown(" ".join(f":blue-badge[{md_safe(t_service(s.split('(')[0].strip()))}]" for s in services))

        languages = t_data(site.languages) if site.languages else t("not_listed")
        insurance = t_data(site.insurance_note) if site.insurance_note else t("not_listed")
        st.markdown(f":material/translate: **{t('languages_label')}:** {md_safe(languages)}")
        st.markdown(f":material/verified_user: **{t('insurance_label')}:** {md_safe(insurance)}")

        if st.button(t("book_button"), icon=":material/event_available:",
                     key=f"book_{position}_{site.site_key}", type="primary"):
            st.session_state["selected_site"] = {
                "name": site.name, "address": site.address, "city": site.city, "zip5": site.zip5,
                "phone": site.phone, "languages": site.languages, "insurance_note": site.insurance_note,
            }
            st.switch_page("book_page.py")


# ---------------------------------------------------------------- page
top = st.columns([3, 2], vertical_alignment="bottom")
with top[1]:
    language_picker("search")          # first, so the rest uses the chosen language
apply_direction()
with top[0]:
    st.title(f":material/explore: {t('app_title')}")
st.caption(t("tagline"))

services, clinic_languages = load_options()
saved = st.session_state.get("search", {})

service_options = ["Any"] + services
language_options = ["Any"] + clinic_languages
group_options = list(SITE_GROUPS)


def pick(options, value, default=0):
    return options.index(value) if value in options else default


with st.form("search_form", border=True):
    row1 = st.columns(2)
    zip_code = row1[0].text_input(
        t("zip_label"), value=saved.get("zip", ""), max_chars=5,
        placeholder=t("zip_placeholder"), key="f_zip",
    )
    service = row1[1].selectbox(
        t("service_label"), service_options, index=pick(service_options, saved.get("service")),
        format_func=lambda v: t("service_any") if v == "Any" else t_service(v), key="f_service",
    )
    row2 = st.columns(2)
    group = row2[0].selectbox(
        t("site_type_label"), group_options, index=pick(group_options, saved.get("group")),
        format_func=lambda v: t(SITE_GROUPS[v]), key="f_group",
    )
    language = row2[1].selectbox(
        t("clinic_language_label"), language_options, index=pick(language_options, saved.get("language")),
        format_func=lambda v: t("clinic_language_any") if v == "Any" else v, key="f_language",
    )
    browse = st.toggle(t("browse_toggle"), value=saved.get("browse", False), key="f_browse")
    submitted = st.form_submit_button(t("search_button"), icon=":material/search:", type="primary")

if submitted:
    st.session_state["search"] = {
        "zip": zip_code.strip(), "service": service, "group": group, "language": language,
        "browse": browse,
    }

params = st.session_state.get("search")
if not params:
    st.info(t("start_prompt"), icon=":material/pin_drop:")
else:
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
        # Quick toggle under the form: changing it re-shows results instantly, no new search.
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
