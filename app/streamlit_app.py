import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

st.title("🎬 IMDb 2024 Movie Analysis Dashboard")

# Connect to MySQL
engine = create_engine("mysql+pymysql://root@localhost/imdb_db")

df = pd.read_sql("SELECT * FROM movies", engine)

st.subheader("Dataset Preview")
st.dataframe(df)

# ---------------- FILTERS ----------------

st.sidebar.header("Interactive Filters")

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

duration_filter = st.sidebar.slider(
    "Maximum Duration",
    int(df["Duration"].min()),
    int(df["Duration"].max()),
    int(df["Duration"].max())
)

genre_filter = st.sidebar.multiselect(
    "Select Genre",
    options=df["Genre"].unique(),
    default=df["Genre"].unique()
)

filtered_df = df[
    (df["Ratings"] >= rating_filter) &
    (df["Voting Counts"] >= votes_filter) &
    (df["Duration"] <= duration_filter) &
    (df["Genre"].isin(genre_filter))
]

st.subheader("Filtered Movies")
st.dataframe(filtered_df)

# ---------------- TOP RATED MOVIES ----------------

st.subheader("Top 10 Movies by Rating")

top_movies = df.sort_values("Ratings", ascending=False).head(10)

fig1, ax1 = plt.subplots()
ax1.barh(top_movies["Movie Name"], top_movies["Ratings"])
ax1.set_xlabel("Rating")

st.pyplot(fig1)

# ---------------- GENRE DISTRIBUTION ----------------

st.subheader("Genre Distribution")

genre_counts = df["Genre"].value_counts()

fig2, ax2 = plt.subplots()
genre_counts.plot(kind="bar", ax=ax2)

st.pyplot(fig2)

# ---------------- AVERAGE RATING BY GENRE ----------------

st.subheader("Average Rating by Genre")

avg_rating = df.groupby("Genre")["Ratings"].mean()

fig3, ax3 = plt.subplots()
avg_rating.plot(kind="bar", ax=ax3)

st.pyplot(fig3)

# ---------------- RATING DISTRIBUTION ----------------

st.subheader("Rating Distribution")

fig4, ax4 = plt.subplots()
sns.histplot(df["Ratings"], bins=10, ax=ax4)

st.pyplot(fig4)

# ---------------- VOTING TRENDS ----------------

st.subheader("Average Voting Counts by Genre")

votes_by_genre = df.groupby("Genre")["Voting Counts"].mean()

fig5, ax5 = plt.subplots()
votes_by_genre.plot(kind="bar", ax=ax5)

st.pyplot(fig5)

# ---------------- VOTES VS RATINGS ----------------

st.subheader("Votes vs Ratings")

fig6, ax6 = plt.subplots()
sns.scatterplot(data=df, x="Voting Counts", y="Ratings", ax=ax6)

st.pyplot(fig6)

# ---------------- DURATION EXTREMES ----------------

st.subheader("Shortest and Longest Movies")

shortest = df.loc[df["Duration"].idxmin()]
longest = df.loc[df["Duration"].idxmax()]

st.write("Shortest Movie")
st.write(shortest)

st.write("Longest Movie")
st.write(longest)