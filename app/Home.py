"""Compass Care: start here.

Run from the project's top folder with:
    streamlit run app/Home.py
"""

import streamlit as st

st.set_page_config(
    page_title="Compass Care",
    page_icon=":material/explore:",
    layout="centered",
)

pages = [
    st.Page("search_page.py", title="Search", icon=":material/search:", url_path="search", default=True),
    st.Page("book_page.py", title="Book an appointment", icon=":material/event_available:", url_path="book"),
]

# The two pages link to each other with buttons, so the sidebar menu stays hidden.
st.navigation(pages, position="hidden").run()
