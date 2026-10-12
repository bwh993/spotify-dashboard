import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Page Setup ----------
st.set_page_config(page_title="Spotify Top100 Dashboard")
st.title("Spotify Top100 Dashboard | Team 3:Wenbo Hu, Yuhan Dang, Yanxi Wang, Borui Su")
st.caption("Dashboard for Spotify content managers, to select trending songs for official curated playlists.")

# ---------- Load Data ----------
@st.cache_data
def load_data():
    longevity_df = pd.read_csv("chart_longevity_panel.csv")
    meta_df = pd.read_csv("track_metadata.csv")
    combined_df = pd.merge(longevity_df, meta_df, on="track_id", how="left")
    combined_df = combined_df.dropna(subset=["genre"])
    return combined_df

df = load_data()

# ---------- Genre Filter ----------
genres = df["genre"].unique()
selected_genre = st.selectbox("Select Genre", ["All"] + sorted(genres))
if selected_genre != "All":
    df_filtered = df[df["genre"] == selected_genre]
else:
    df_filtered = df

# ---------- KPI Metrics ----------
avg_longevity = df_filtered["weeks_on_top_100"].mean()
pct_over8 = (df_filtered["weeks_on_top_100"] > 8).mean() * 100
median_peak = df_filtered["peak_chart_rank"].median()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Weeks on Top100", f"{avg_longevity:.1f}")
with col2:
    st.metric("% Tracks >8 Weeks", f"{pct_over8:.1f} %")
with col3:
    st.metric("Median Peak Chart Rank", f"{median_peak:.0f}")

# ---------- Histogram Chart ----------
fig = px.histogram(
    df_filtered,
    x="weeks_on_top_100",
    title="Distribution of Weeks Tracks Stay on Spotify Top 100"
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Footer Note ----------
st.divider()
# 你后面可以自己修改年份，现在先用占位，不影响运行
st.write("Data: 2018 – 2026, Kaggle static snapshot. Production refresh frequency: weekly.")
st.caption("Note: Average longevity is pulled down by many short-lived 1–2 week viral hit outliers.")


