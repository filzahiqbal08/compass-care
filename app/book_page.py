"""Page 2: how to book at the clinic you picked (phone number first)."""

import re
from urllib.parse import quote

import streamlit as st

from common import md_safe
from i18n import apply_direction, language_picker, t, t_data

top = st.columns([3, 2], vertical_alignment="bottom")
with top[1]:
    language_picker("book")
apply_direction()
with top[0]:
    st.title(f":material/event_available: {t('book_title')}")

site = st.session_state.get("selected_site")

if not site:
    st.info(t("no_clinic_selected"))
else:
    st.markdown(f"### {md_safe(site['name'])}")
    st.markdown(f":material/location_on: {md_safe(site['address'])}, {md_safe(site['city'])} {site['zip5']}")
    st.caption(t("book_intro"))

    phone = site.get("phone")
    if phone:
        digits = re.sub(r"[^\d+]", "", phone)
        # The number is shown as text too, because "tap to call" only works on phones.
        st.markdown(f"## :material/call: {phone}")
        st.link_button(t("call_button", phone=phone), f"tel:{digits}", icon=":material/call:", type="primary")
    else:
        st.warning(t("phone_not_listed"), icon=":material/call_end:")

    destination = quote(f"{site['name']}, {site['address']}, {site['city']}, CA {site['zip5']}")
    st.link_button(
        t("directions_button"),
        f"https://www.google.com/maps/dir/?api=1&destination={destination}",
        icon=":material/directions:",
    )

    with st.container(border=True):
        st.markdown(f"**{t('ask_title')}**")
        for key in ("ask_1", "ask_2", "ask_3", "ask_4"):
            st.markdown(f"- {t(key)}")
        languages = t_data(site["languages"]) if site.get("languages") else t("not_listed")
        insurance = t_data(site["insurance_note"]) if site.get("insurance_note") else t("not_listed")
        st.markdown(f":material/translate: **{t('languages_label')}:** {md_safe(languages)}")
        st.markdown(f":material/verified_user: **{t('insurance_label')}:** {md_safe(insurance)}")
    st.caption(t("book_confirm_note"))

if st.button(t("back_button"), icon=":material/arrow_back:"):
    st.switch_page("search_page.py")

st.caption(t("footer"))
