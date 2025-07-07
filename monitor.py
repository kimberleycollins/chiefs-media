import streamlit as st
import requests
from datetime import datetime, date

# --- CONFIG ---
API_KEY = '403ed40c75cd146c59aeaef391538f4e'
BASE_URL = 'https://gnews.io/api/v4/search'

# --- SIDEBAR ---
st.sidebar.title("📰 Media Monitoring Tool")

query_input = st.sidebar.text_input("Enter search text (e.g. Gallagher Chiefs)", "Gallagher Chiefs")
exact_phrase = st.sidebar.checkbox("Search as exact phrase", value=True)

lang = st.sidebar.selectbox("Language", ["en", "es", "fr", "de", "zh"])
max_articles = st.sidebar.slider("Number of articles to fetch", 5, 30, 10)

start_date = st.sidebar.date_input("Start date", date.today())
end_date = st.sidebar.date_input("End date", date.today())

# Format query
query = f'"{query_input}"' if exact_phrase else query_input

# --- MAIN ---
st.title("📡 Real-Time News Monitor")
st.markdown(f"### Searching for: `{query}`")
st.markdown(f"**Date range:** {start_date} to {end_date}")

def fetch_articles(query, lang, max_articles, from_date, to_date):
    params = {
        'q': query,
        'token': API_KEY,
        'lang': lang,
        'max': max_articles,
        'from': from_date.isoformat(),
        'to': to_date.isoformat(),
        'sortBy': 'publishedAt'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        st.error(f"API Error: {response.status_code} — {response.text}")
        return []

articles = fetch_articles(query, lang, max_articles, start_date, end_date)

# --- DISPLAY ---
if articles:
    for article in articles:
        st.subheader(article['title'])
        pub_time = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00')).strftime('%d %b %Y, %I:%M %p')
        st.write(f"*Source: {article['source']['name']}*  —  *Published: {pub_time}*")
        st.write(article['description'])
        st.markdown(f"[Read more]({article['url']})")
        st.markdown("---")
else:
    st.info("No articles found.")
