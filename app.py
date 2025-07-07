import streamlit as st
import feedparser
from datetime import datetime
import pandas as pd

# --- SIDEBAR ---
st.sidebar.title("📰 Google News Monitor")
query_input = st.sidebar.text_input(
    "Enter search terms",
    '"Gallagher Chiefs" OR "Chiefs Rugby Club"'
)
sort_by = st.sidebar.selectbox(
    "Sort by",
    ["Date (Newest First)", "Date (Oldest First)", "Outlet (A-Z)", "Outlet (Z-A)"]
)

# --- BUILD GOOGLE NEWS RSS URL ---
rss_url = f"https://news.google.com/rss/search?q={query_input.replace(' ', '+')}&hl=en-NZ&gl=NZ&ceid=NZ:en"

# --- MAIN PAGE ---
st.title("📡 Google News Feed Monitor")
st.markdown(f"### Results for: `{query_input}`")
st.markdown(f"🔗 [View directly in Google News]({rss_url.replace('/rss/', '/search/')})")

# --- FETCH & PARSE FEED ---
feed = feedparser.parse(rss_url)

# --- CONVERT TO DATAFRAME ---
articles = []
for entry in feed.entries:
    published = datetime(*entry.published_parsed[:6]) if entry.get("published_parsed") else None
    source = entry.source.title if "source" in entry else "Unknown"
    articles.append({
        "title": entry.title,
        "summary": entry.summary,
        "link": entry.link,
        "published": published,
        "source": source
    })

df = pd.DataFrame(articles)

# --- SORT ---
if sort_by == "Date (Newest First)":
    df = df.sort_values(by="published", ascending=False)
elif sort_by == "Date (Oldest First)":
    df = df.sort_values(by="published", ascending=True)
elif sort_by == "Outlet (A-Z)":
    df = df.sort_values(by="source", ascending=True)
elif sort_by == "Outlet (Z-A)":
    df = df.sort_values(by="source", ascending=False)

# --- DISPLAY ---
if not df.empty:
    for _, row in df.iterrows():
        st.subheader(row["title"])
        if row["published"]:
            st.write(f"*Published: {row['published'].strftime('%d %b %Y, %I:%M %p')}*")
        st.write(f"*Source: {row['source']}*")
        st.write(row["summary"], unsafe_allow_html=True)
        st.markdown(f"[Read more]({row['link']})")
        st.markdown("---")
else:
    st.info("No articles found.")
