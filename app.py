
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="IPL Dashboard", layout="wide")

st.title("🏏 IPL Data Analysis Dashboard")
st.markdown("## 📊 Interactive IPL Analytics")
st.markdown("---")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv", usecols=['batter', 'total_runs'])
    return matches, deliveries

matches, deliveries = load_data()

# -------------------------------
# KPI Cards
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", len(matches))
col2.metric("Total Teams", matches['team1'].nunique())
col3.metric("Total Players", deliveries['batter'].nunique())

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filters")

teams = sorted(matches['team1'].dropna().unique())
selected_team = st.sidebar.selectbox("Select Team", teams)

if 'season' in matches.columns:
    seasons = sorted(matches['season'].dropna().unique())
    selected_season = st.sidebar.selectbox("Select Season", seasons)
    matches = matches[matches['season'] == selected_season]

player = st.sidebar.selectbox("Select Player", deliveries['batter'].unique())

# -------------------------------
# Show Data
# -------------------------------
if st.checkbox("Show Matches Data"):
    st.dataframe(matches)

# -------------------------------
# Team Matches
# -------------------------------
team_matches = matches[
    (matches['team1'] == selected_team) |
    (matches['team2'] == selected_team)
]

st.subheader(f"📌 Matches of {selected_team}")
st.dataframe(team_matches)

# -------------------------------
# Team vs Team
# -------------------------------
st.subheader("🆚 Team vs Team")

team1 = st.selectbox("Team 1", teams, key="team1")
team2 = st.selectbox("Team 2", teams, key="team2")

vs_matches = matches[
    ((matches['team1'] == team1) & (matches['team2'] == team2)) |
    ((matches['team1'] == team2) & (matches['team2'] == team1))
]

st.dataframe(vs_matches)

# -------------------------------
# Win Count (Bar Chart)
# -------------------------------
st.subheader("🏆 Win Count")

fig1, ax1 = plt.subplots()
matches['winner'].value_counts().plot(kind='bar')
plt.xticks(rotation=90)
st.pyplot(fig1)

# -------------------------------
# Pie Chart (Top Teams)
# -------------------------------
st.subheader("🥧 Top 5 Teams Win Distribution")

fig2, ax2 = plt.subplots()
matches['winner'].value_counts().head(5).plot(kind='pie', autopct='%1.1f%%')
st.pyplot(fig2)

# -------------------------------
# Top Batsmen
# -------------------------------
st.subheader("🔥 Top 10 Batsmen")

top_batsman = deliveries.groupby('batter')['total_runs'].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()
sns.barplot(x=top_batsman.values, y=top_batsman.index)
st.pyplot(fig3)

# -------------------------------
# Orange Cap
# -------------------------------
top_player = deliveries.groupby('batter')['total_runs'].sum().idxmax()
top_runs = deliveries.groupby('batter')['total_runs'].sum().max()

st.subheader("🟠 Orange Cap Holder")
st.write(f"{top_player} - {top_runs} runs")

# -------------------------------
# Player Performance
# -------------------------------
st.subheader(f"🎯 Performance of {player}")

player_runs = deliveries[deliveries['batter'] == player]['total_runs'].sum()
st.write(f"Total Runs: {player_runs}")

# -------------------------------
# Matches per Season
# -------------------------------
if 'season' in matches.columns:
    st.subheader("📅 Matches per Season")

    fig4, ax4 = plt.subplots()
    matches['season'].value_counts().sort_index().plot(kind='line', marker='o')
    st.pyplot(fig4)

# -------------------------------
# Toss Analysis
# -------------------------------
if 'toss_winner' in matches.columns:
    st.subheader("🪙 Toss Winners")
    st.bar_chart(matches['toss_winner'].value_counts())

# -------------------------------
# City Analysis
# -------------------------------
if 'city' in matches.columns:
    st.subheader("📍 Matches by City")
    st.bar_chart(matches['city'].value_counts().head(10))

# -------------------------------
# Search Player
# -------------------------------
search = st.text_input("🔎 Search Player")

if search:
    result = deliveries[deliveries['batter'].str.contains(search, case=False)]
    st.write(result.head())

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.write("Created using Streamlit | IPL Dataset from Kaggle")