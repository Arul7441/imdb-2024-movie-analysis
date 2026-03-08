import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Page title
st.title("🎬 IMDb 2024 Movie Analysis Dashboard")

# Connect to MySQL
engine = create_engine("mysql+pymysql://root@localhost/imdb_db")

# Load dataset
df = pd.read_sql("SELECT * FROM movies", engine)

st.subheader("Dataset Preview")
st.dataframe(df)

# Sidebar filters
st.sidebar.header("Filters")

rating_filter = st.sidebar.slider(
    "Minimum Rating",
    float(df["Ratings"].min()),
    float(df["Ratings"].max()),
    6.0
)

votes_filter = st.sidebar.slider(
    "Minimum Votes",
    int(df["Voting Counts"].min()),
    int(df["Voting Counts"].max()),
    10000
)

filtered_df = df[
    (df["Ratings"] >= rating_filter) &
    (df["Voting Counts"] >= votes_filter)
]

st.subheader("Filtered Movies")
st.dataframe(filtered_df)

# -------- Chart 1 Top Rated Movies --------

st.subheader("Top 10 Movies by Rating")

top_movies = df.sort_values("Ratings", ascending=False).head(10)

fig1, ax1 = plt.subplots()
ax1.barh(top_movies["Movie Name"], top_movies["Ratings"])
ax1.set_xlabel("Rating")
ax1.set_ylabel("Movie")

st.pyplot(fig1)

# -------- Chart 2 Rating Distribution --------

st.subheader("Rating Distribution")

fig2, ax2 = plt.subplots()
sns.histplot(df["Ratings"], bins=10, ax=ax2)

st.pyplot(fig2)

# -------- Chart 3 Votes vs Ratings --------

st.subheader("Votes vs Ratings")

fig3, ax3 = plt.subplots()
sns.scatterplot(data=df, x="Voting Counts", y="Ratings", ax=ax3)

st.pyplot(fig3)

# -------- Chart 4 Top Voted Movies --------

st.subheader("Top 10 Movies by Voting Counts")

top_votes = df.sort_values("Voting Counts", ascending=False).head(10)

fig4, ax4 = plt.subplots()
ax4.barh(top_votes["Movie Name"], top_votes["Voting Counts"])

st.pyplot(fig4)

# -------- Chart 5 Correlation --------

st.subheader("Correlation Between Ratings and Votes")

correlation = df[["Ratings", "Voting Counts"]].corr()

fig5, ax5 = plt.subplots()
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax5)

st.pyplot(fig5)