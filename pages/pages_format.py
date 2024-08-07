from st_pages import Page, Section, add_indentation, show_pages


def pages_format():
    show_pages(
        [
            Page("streamlit_app.py", "Home", "🏠", in_section=False),
            Page("pages/styler.py", "Styler objects", "🎨", in_section=False),
            Page("pages/aggrid.py", "AdGrid", "🌐", in_section=False),
        ]
    )
    add_indentation()   # Function that looks at the in_section parameter
