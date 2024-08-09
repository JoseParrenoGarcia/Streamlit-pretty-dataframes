from st_pages import Page, Section, add_indentation, show_pages


def pages_format():
    show_pages(
        [
            Page("streamlit_app.py", "Home", "🏠"),
            Page("pages/styler.py", "Styler objects", "🎨"),
            Page("pages/aggrid.py", "AdGrid", "🌐"),
        ]
    )
