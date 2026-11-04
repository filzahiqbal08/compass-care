"""Every English sentence the app shows, in one place.

Other languages use the same keys in translations.json (see i18n.py).
To change any wording, edit it here. Keep placeholders like {n} and {phone}
exactly as written, because the app fills them in.
"""

EN = {
    # Header
    "app_title": "Compass Care",
    "tagline": "Find a clinic near you in San Diego County",
    "language_label": "Language",
    "translation_coming": "This language is coming soon. Showing English for now.",

    # Search form
    "zip_label": "ZIP code",
    "zip_placeholder": "e.g. 92105",
    "site_type_label": "Type of site",
    "service_label": "What do you need?",
    "service_any": "Any service",
    "clinic_language_label": "Language you need at the clinic",
    "clinic_language_any": "Any language",
    "count_label": "Show",
    "browse_toggle": "Browse all clinics in San Diego County (ignores ZIP code)",
    "browse_summary": "Showing all {matches} matching sites in San Diego County, A to Z",
    "count_all": "All",
    "search_button": "Search",
    "start_prompt": "Enter a ZIP code to find nearby clinics.",

    # Types of site
    "site_public": "Public sites (recommended)",
    "site_all": "All sites",
    "site_health_center": "Health centers",
    "site_hospital": "Hospitals",
    "site_referral": "Referral-only (a doctor must refer you)",
    "site_school": "School-based clinics",

    # Messages
    "msg_invalid_zip": "Please enter all 5 digits of your ZIP code (for example, 92105).",
    "msg_zip_not_found": "We couldn't find that ZIP code. Please check the digits. Compass Care currently covers San Diego County only.",
    "msg_outside_county": "That ZIP code is outside San Diego County. Compass Care currently covers San Diego County only.",
    "msg_fallback_none": "No sites match your search. Here are the nearest health centers instead. Call to ask what they offer.",
    "msg_fallback_some": "Only {n} sites match your search. We added the nearest health centers below. Call to ask what they offer.",
    "msg_fallback_one": "Only 1 site matches your search. We added the nearest health centers below. Call to ask what they offer.",
    "msg_no_results": "No sites found. Try choosing \"Any service\" or \"Any language\".",
    "results_summary": "Showing {shown} of {matches} matching sites near {zip}",

    # Result cards
    "fallback_tag": "Nearest alternative",
    "miles_away": "{miles} mi away",
    "languages_label": "Languages",
    "insurance_label": "Insurance",
    "not_listed": "Not listed. Call to ask.",
    "phone_not_listed": "Phone not listed",
    "book_button": "Book appointment",

    # Booking page
    "book_title": "Book an appointment",
    "book_intro": "Call the clinic to book. Online booking isn't available yet.",
    "call_button": "Call {phone}",
    "directions_button": "Get directions",
    "back_button": "Back to results",
    "no_clinic_selected": "Pick a clinic on the search page first.",
    "ask_title": "When you call, you can ask:",
    "ask_1": "Is there a staff member or interpreter who speaks my language?",
    "ask_2": "Which insurance plans do you accept?",
    "ask_3": "Do you offer lower-cost care if I don't have insurance?",
    "ask_4": "What should I bring to my visit?",
    "book_confirm_note": "Hours and details can change, so confirm everything when you call.",

    # Footer
    "footer": "Clinic information comes from the federal government's list of health centers and other public sources. Please call ahead to confirm hours, insurance and languages.",
}
