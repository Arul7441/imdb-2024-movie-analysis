import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

st.set_page_config(page_title="IMDb 2024 Dashboard", layout="wide")

st.title("🎬 IMDb 2024 Movie Analysis Dashboard")

# ---------------- DATABASE CONNECTION ----------------

engine = create_engine("mysql+pymysql://root@localhost/imdb_db")

df = pd.read_sql("SELECT * FROM movies", engine)

# ---------------- CLEAN DATA ----------------

df["Ratings"] = pd.to_numeric(df["Ratings"], errors="coerce")

df["Voting Counts"] = (
    df["Voting Counts"]
    .astype(str)
    .str.replace(",", "")
    .str.replace("(", "")
    .str.replace(")", "")
    .str.replace("K", "000")
)

df["Voting Counts"] = pd.to_numeric(df["Voting Counts"], errors="coerce")

df["Duration"] = df["Duration"].astype(str).str.replace("min", "")
df["Duration"] = pd.to_numeric(df["Duration"], errors="coerce")

df["Ratings"] = df["Ratings"].fillna(0)
df["Voting Counts"] = df["Voting Counts"].fillna(0)
df["Duration"] = df["Duration"].fillna(0)
df["Genre"] = df["Genre"].fillna("Unknown")

# ---------------- EXPLODE GENRES ----------------

genre_series = df["Genre"].str.split(",")

genre_exploded = genre_series.explode().str.strip()

# Standardize genre names (combine similar ones)
genre_exploded = genre_exploded.replace({
    "Sci Fi": "Sci-Fi",
    "Science Fiction": "Sci-Fi",
    "Rom-Com": "Romance",
    "Biography": "Biopic"
})

df_genre = df.copy()
df_genre["Genre"] = df_genre["Genre"].str.split(",")
df_genre = df_genre.explode("Genre")
df_genre["Genre"] = df_genre["Genre"].str.strip()

df_genre["Genre"] = df_genre["Genre"].replace({
    "Sci Fi": "Sci-Fi",
    "Science Fiction": "Sci-Fi",
    "Rom-Com": "Romance",
    "Biography": "Biopic"
})

# ---------------- DATASET PREVIEW ----------------

st.subheader("Dataset Preview")
st.dataframe(df)

# ---------------- SIDEBAR FILTERS ----------------

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

min_duration = int(df["Duration"].dropna().min())
max_duration = int(df["Duration"].dropna().max())

if min_duration < max_duration:
    duration_filter = st.sidebar.slider(
        "Maximum Duration",
        min_duration,
        max_duration,
        max_duration
    )
else:
    duration_filter = max_duration
    st.sidebar.write("Duration filter unavailable")

# Limit genres to top 25
top_genres = df_genre["Genre"].value_counts().head(25).index.tolist()

genre_filter = st.sidebar.multiselect(
    "Select Genre",
    options=top_genres,
    default=top_genres
)

# Apply filters
filtered_df = df[
    (df["Ratings"] >= rating_filter) &
    (df["Voting Counts"] >= votes_filter) &
    (df["Duration"] <= duration_filter)
]

filtered_df = filtered_df[
    filtered_df["Genre"].str.contains("|".join(genre_filter))
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

genre_counts = df_genre["Genre"].value_counts().head(10)

fig2, ax2 = plt.subplots()

genre_counts.plot(kind="bar", ax=ax2)

ax2.set_xlabel("Genre")

ax2.set_ylabel("Number of Movies")

st.pyplot(fig2)

# ---------------- AVERAGE RATING BY GENRE ----------------

st.subheader("Average Rating by Genre")

avg_rating = df_genre.groupby("Genre")["Ratings"].mean().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()

avg_rating.plot(kind="bar", ax=ax3)

ax3.set_ylabel("Average Rating")

st.pyplot(fig3)

# ---------------- RATING DISTRIBUTION ----------------

st.subheader("Rating Distribution")

fig4, ax4 = plt.subplots()

sns.histplot(df["Ratings"], bins=10, ax=ax4)

st.pyplot(fig4)

# ---------------- VOTES VS RATINGS ----------------

st.subheader("Votes vs Ratings")

fig5, ax5 = plt.subplots()

sns.scatterplot(data=df, x="Voting Counts", y="Ratings", ax=ax5)

st.pyplot(fig5)

# ---------------- TOP VOTED MOVIES ----------------

st.subheader("Top 10 Movies by Voting Counts")

top_votes = df.sort_values("Voting Counts", ascending=False).head(10)

fig6, ax6 = plt.subplots()

ax6.barh(top_votes["Movie Name"], top_votes["Voting Counts"])

st.pyplot(fig6)

# ---------------- CORRELATION HEATMAP ----------------

st.subheader("Correlation Between Ratings and Votes")

corr = df[["Ratings", "Voting Counts"]].corr()

fig7, ax7 = plt.subplots()

sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax7)

st.pyplot(fig7)