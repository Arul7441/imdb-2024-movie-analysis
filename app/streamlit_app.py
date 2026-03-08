import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Connect to MySQL
engine = create_engine("mysql+pymysql://root@localhost/imdb_db")

# Load dataset
df = pd.read_sql("SELECT * FROM movies", engine)

st.title("🎬 IMDb 2024 Movie Dashboard")

st.write("Dataset Preview")
st.dataframe(df)

# ---------- Filters ----------

st.sidebar.header("Filter Movies")

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
    1000
)

filtered_df = df[
    (df["Ratings"] >= rating_filter) &
    (df["Voting Counts"] >= votes_filter)
]

st.subheader("Filtered Movies")
st.dataframe(filtered_df)

# ---------- Top Rated Movies ----------

st.subheader("Top 10 Movies by Rating")

top_movies = df.sort_values("Ratings", ascending=False).head(10)

st.dataframe(top_movies)

# ---------- Rating Distribution ----------

st.subheader("Rating Distribution")

fig, ax = plt.subplots()
sns.histplot(df["Ratings"], bins=10, ax=ax)

st.pyplot(fig)

# ---------- Votes vs Ratings ----------

st.subheader("Votes vs Ratings")

fig2, ax2 = plt.subplots()
sns.scatterplot(data=df, x="Voting Counts", y="Ratings", ax=ax2)

st.pyplot(fig2)