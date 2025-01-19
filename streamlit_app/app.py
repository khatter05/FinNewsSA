import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("Financial News Analysis")

query = st.text_input("Enter your search query:", "stock")

if st.button("Analyze"):
    with st.spinner("Fetching and analyzing news..."):
        response = requests.get(f"{BASE_URL}/analyze_news/", params={"query": query})

    if response.status_code == 200:
        results = response.json()
        for news in results:
            st.subheader(news["title"])
            st.write("**Source:**", news["source"])
            st.write("**Description:**", news["desc"] if news["desc"] else "No description available.")
            st.write("**Entities:**")
            if news["entities"]:
                for entity in news["entities"]:
                    st.markdown(f"- {entity}")
            else:
                st.write("No entities found.")
            st.write("**Sentiment:**", news["sentiment"])
    else:
        st.error("Error fetching news!")
