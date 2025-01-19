import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.title("Financial News Analysis")

# Session state initialization
if "results" not in st.session_state:
    st.session_state.results = []
if "next_page_token" not in st.session_state:
    st.session_state.next_page_token = None
if "previous_page_tokens" not in st.session_state:
    st.session_state.previous_page_tokens = []
if "page" not in st.session_state:
    st.session_state.page = 1

# Fetch and update news results
def fetch_news(query="stocks",page_token=None):
    params = {"query": query}
    if page_token:
        params["page"] = page_token

    response = requests.get(f"{BASE_URL}/analyze_news/", params=params)
    if response.status_code == 200:
        data = response.json()
        st.session_state.results = data.get("results", [])
        st.session_state.next_page_token = data.get("next_page", None)
    else:
        st.error("Error fetching news. Please try again later.")

# Input for query and Analyze button
query = st.text_input("Enter your search query:", "stock")

if st.button("Analyze"):
    with st.spinner("Fetching and analyzing news..."):
        # Reset states on a new query
        st.session_state.page = 1
        st.session_state.previous_page_tokens = []
        fetch_news(query=query)

# Display news results
if st.session_state.results:
    st.write(f"### Page {st.session_state.page}")
    for news in st.session_state.results:
        title_with_link = f"[{news.get('title', 'No Title')}]({news.get('link', '#')})"
        st.markdown(f"### {title_with_link}")
        st.write("**Source:**", news.get("source", "Unknown"))
        st.write("**Publish Date:**", news.get("publish_date", "Unknown"))
        st.write("**Description:**", news.get("desc", "No description available."))
        st.write("**Entities:**")
        if news.get("entities"):
            for entity in news["entities"]:
                st.markdown(f"- {entity}")
        else:
            st.write("No entities found.")
        st.write("**Sentiment:**", news.get("sentiment", "Unknown").capitalize())
        st.write("---")

    # Pagination controls
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.session_state.page > 1 and st.button("Previous Page"):
            st.session_state.page -= 1
            # Fetch previous page
            if st.session_state.previous_page_tokens:
                last_page_token = st.session_state.previous_page_tokens.pop()
                fetch_news(query=query,page_token=last_page_token)

    with col2:
        if st.session_state.next_page_token and st.button("Next Page"):
            st.session_state.page += 1
            # Store current next_page_token in previous pages before updating
            st.session_state.previous_page_tokens.append(st.session_state.next_page_token)
            fetch_news(query=query,page_token=st.session_state.next_page_token)
else:
    st.write("No results available. Please click Analyze to fetch news.")
