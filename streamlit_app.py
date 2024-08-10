import streamlit as st

# ---------------------------------------------------------------------
# HOME PAGE - CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    layout="wide",
)

st.title('Creating beautiful streamlit tables.')

st.write('')
st.subheader("What")
st.write('This app will show you a few methods of styling dataframes in your streamlit app. We will cover:')
st.markdown("- standard Styler objects \n"
            "- the AdGrid package \n"
            )

st.write('')
st.subheader("Considerations")
st.write('Of course, things might have changed depending on when you are reading/checking this app. For example,'
         'as of August 2024, I wrote the app based on the following package versions.')

st.markdown("- streamlit==1.32.0 \n"
            "- pandas==2.2.2 \n"
            "- matplotlib==3.9.0 \n"
            "- streamlit-aggrid==1.0.5 \n"

            )

st.write('')
st.subheader("Details")
st.write("If you wish to check the exact code which generated this app, feel free to check the GitHub repo "
         "associated with the app.")
st.link_button("GitHub repo", "https://github.com/JoseParrenoGarcia/Streamlit-pretty-dataframes")
