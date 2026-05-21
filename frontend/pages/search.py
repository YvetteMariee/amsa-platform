import streamlit as st
import requests

st.title("Search PDF")

query = st.text_input("Recherche")

if st.button("Search"):
    response = requests.get(
        "http://localhost:8000/search",
        params={"q": query}
    )

    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("Erreur backend")