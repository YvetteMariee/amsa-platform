import streamlit as st

st.set_page_config(
    page_title="AMSA Platform",
    layout="wide"
)

st.title("AMSA Intelligent Monitoring Platform")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Pages",
    [
        "Dashboard",
        "Upload",
        "Search",
        "Alerts",
        "Reports"
    ]
)

if page == "Dashboard":
    st.header("Dashboard")

elif page == "Upload":
    st.header("Upload Documents")

elif page == "Search":
    st.header("Search Engine")

elif page == "Alerts":
    st.header("Alerts Management")

elif page == "Reports":
    st.header("Reports")