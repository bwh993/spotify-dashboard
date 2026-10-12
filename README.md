# Spotify Top 100 Chart Longevity Dashboard
This project creates a Streamlit dashboard to analyze how long songs remain inside Spotify’s Top 100 chart.

## Step 1: Dataset and Decision-Maker
### Dataset details
I chose a tabular synthetic Kaggle dataset about Spotify Top 100 songs, split into two small CSV files (`chart_longevity_panel.csv` and `track_metadata.csv`). Combined file size is far below 25MB, so it works for GitHub and Streamlit Cloud.
Dataset link: https://www.kaggle.com/datasets/vedauv/global-spotify-hits-and-audio-dynamics-20182026/data

One row represents one unique song identified by `track_id`.
- `chart_longevity_panel.csv`: chart metrics like peak rank, weeks on chart, total streams
- `track_metadata.csv`: song info including genre, artist and release date

The dataset spans multiple years of Top 100 entries. I read the Kaggle page to confirm data source, columns and whether it was synthetic.

### Decision-Maker
This dashboard is made for a **Spotify content manager who builds official curated playlists**. Their job is to select songs that stay popular for long-running playlists, so this tool is only built for their workflow, not for all users.


## Step 2: Justify the Dashboard
1. Who looks at it, and how often?
The dashboard is viewed by the Spotify content manager for curated playlists. They check it **weekly**, every time they update and refresh long-running official playlists.

2. What decision does it support?
If the Spotify content manager sees that a genre or track group has consistently long chart longevity on this dashboard, they will add more songs of that type to their permanent curated playlists.

3. What do they do today without it — and what does that cost them in time, money, or mistakes?
Without this dashboard, they manually download and filter raw CSV chart data in spreadsheets. This takes several hours each week. They may miss patterns in genre longevity, leading them to add short-lived trending songs that drop off charts quickly. This reduces playlist listener retention and wastes the playlist slot allocation.

4. Why a dashboard rather than a weekly email, a report, or an alert?
A static weekly email or PDF report cannot be filtered interactively. The manager needs to quickly switch between genres and drill down into track performance every week. An alert only triggers for single events, while this dashboard supports ongoing exploration and comparison across many tracks.

## Step3: Decide What Matters
I first completed EDA using Pandas and Matplotlib, checking dataset shape, data types, missing values, variable distributions, and correlations relevant to track chart longevity.

### Dashboard Components
- 3 headline KPIs shown side-by-side with st.metric: average weeks on chart, share of tracks staying over 8 weeks, median peak rank.
- 1 supporting histogram showing distribution of weeks on chart.
- One filter: genre dropdown, the only filter the playlist manager needs.

### Two things I chose not to show, and why
1. Individual track total stream counts. This looked interesting during EDA, but raw stream volume does not help judge long-term chart staying power. Showing it would not change playlist selection decisions.
2. Explicit content tag for songs. Whether a track contains explicit lyrics is irrelevant for evaluating chart longevity, so it adds unnecessary clutter.

### Potentially misleading data and handling
There are outliers: a small subset of songs remain on the chart for an extremely long time and can skew average metrics. I add a warning caption below the headline numbers to remind the viewer about these outliers. There are no missing time periods or ambiguous columns.

### Page layout
- Top: Genre dropdown filter for interactive exploration
- Middle: headline KPIs for instant high-level summary
- Then: histogram to explain the distribution behind the KPIs.
- No raw data table, as the manager does not need individual row details.
I sketched this layout on paper before coding, and removed any elements that would not affect the manager’s decisions.

## Step4: Decide the Refresh Frequency
The underlying Spotify chart data should refresh **weekly**. New Top100 chart rankings release once per week, and the content manager only updates playlists on a weekly schedule. More frequent refreshes like daily or real-time would add unnecessary system cost and would not change their decisions.

1. Data refresh frequency: Weekly, after the weekly Top100 chart publishes.
2. Review frequency: The Spotify content manager reviews the dashboard **every Monday morning**, right before they adjust the long-running curated playlists. The data refreshes weekly, matching their review cycle.
3. Tracked metric & action trigger: Track the share of tracks that stay on the Top100 chart for over 8 weeks. If this percentage for a genre drops below 30%, the content manager will investigate and reduce adding new songs from that genre into permanent playlists.
4. Cost of stale data: If the dashboard is one week out of date, the manager relies on last week’s chart performance. They may keep adding tracks with rapidly falling longevity, which hurts playlist listener retention. If stale for multiple weeks, the manager will repeatedly pick short-lived songs, wasting limited playlist slots.

On the final dashboard, I will add a caption at the bottom:
> Data: Kaggle static snapshot. In production, data refreshes weekly after new Top100 chart release.
