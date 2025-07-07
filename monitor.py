import streamlit as st
import requests
from datetime import datetime

# --- CONFIG ---
API_KEY = '403ed40c75cd146c59aeaef391538f4e'  # Replace with your actual GNews API key
BASE_URL = 'https://gnews.io/api/v4/search'

# --- SEARCH TERMS ---
search_terms = [
    '"Gallagher Chiefs"',
    '"Chiefs Rugby"',
    '"Jono Gibbes"',
    '"Lalakai Foketi"'
]
query = " OR ".join(search_terms)

# --- SIDEBAR ---
st.sidebar.title("📰 Media Monitoring Tool")
lang = st.sidebar.selectbox("Language", ["en", "es", "fr", "de", "zh"])
max_articles = st.sidebar.slider("Number of articles to fetch", 5, 30, 10)

# --- MAIN ---
st.title("📡 Real-Time News Monitor")
st.markdown("### Searching for any of the following:")
for term in search_terms:
    st.markdown(f"- {term.strip('\"')}")

def fetch_articles(query, lang, max_articles):
    params = {
        'q': query,
        'token': API_KEY,
        'lang': lang,
        'max': max_articles
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        st.error(f"API Error: {response.status_code} — {response.text}")
        return []

articles = fetch_articles(query, lang, max_articles)

if articles:
    for article in articles:
        st.subheader(article['title'])
        st.write(f"*Source: {article['source']['name']}*  —  *Published: {datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00')).strftime('%d %b %Y, %I:%M %p')}*")
        st.write(article['description'])
        st.markdown(f"[Read more]({article['url']})")
        st.markdown("---")
else:
    st.info("No articles found.")
