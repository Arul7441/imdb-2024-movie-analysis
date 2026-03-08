import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/clean_movies.csv")

# Split genres (because movies can have multiple genres)
df["Genre"] = df["Genre"].str.split(",")

# Convert list of genres into rows
df = df.explode("Genre")

# Remove extra spaces
df["Genre"] = df["Genre"].str.strip()

# Save genre-wise CSV files
genres = df["Genre"].unique()

for g in genres:
    genre_df = df[df["Genre"] == g]
    genre_df.to_csv(f"data/{g}_movies.csv", index=False)

# Save merged dataset
df.to_csv("data/merged_movies.csv", index=False)

print("Genre-wise CSV files created successfully!")
print("Genres found:", genres)