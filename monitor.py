import streamlit as st
import feedparser
from datetime import datetime
import pandas as pd

# --- CONFIG ---
query_input = st.sidebar.text_input("Enter search terms", '"Gallagher Chiefs" OR "Chiefs Rugby Club"')
rss_url = f"https://news.google.com/rss/search?q={query_input.replace(' ', '+')}&hl=en-NZ&gl=NZ&ceid=NZ:en"

# --- MAIN ---
st.title("📡 Google News Feed Monitor")
st.markdown(f"### Showing results for: `{query_input}`")

# --- FETCH & PARSE ---
feed = feedparser.parse(rss_url)

# Convert entries to DataFrame for easier sorting
data = []
for entry in feed.entries:
    published = datetime(*entry.published_parsed[:6]) if entry.get("published_parsed") else None
    source = entry.source.title if "source" in entry else "Unknown"
    data.append({
        "title": entry.title,
        "summary": entry.summary,
        "link": entry.link,
        "published": published,
        "source": source
    })

df = pd.DataFrame(data)

# --- SORT OPTIONS ---
sort_by = st.selectbox("Sort by", ["Date (Newest First)", "Date (Oldest First)", "Outlet (A-Z)", "Outlet (Z-A)"])

if sort_by == "Date (Newest First)":
    df = df.sort_values(by="published", ascending=False)
elif sort_by == "Date (Oldest First)":
    df = df.sort_values(by="published", ascending=True)
elif sort_by == "Outlet (A-Z)":
    df = df.sort_values(by="source", ascending=True)
elif sort_by == "Outlet (Z-A)":
    df = df.sort_values(by="source", ascending=False)

# --- DISPLAY RESULTS ---
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
