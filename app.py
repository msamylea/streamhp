
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Document Forensics Suite",
    page_icon="🔍",
    layout="wide"
)

home_page = st.Page('pages/homepage.py', title="Home")
sig_page = st.Page('pages/extract_sigs.py', title="Detect Signatures")
manip_page = st.Page('pages/check_manips.py', title="Confirm Authenticity")
forgery_page = st.Page('pages/forgery_page.py', title="Detect Forgery")
pg = st.navigation([home_page, sig_page, manip_page, forgery_page])

pg.run()