import pandas as pd
import re

# Load scraped data
df = pd.read_csv("data/imdb_movies.csv")

print("Original Data")
print(df.head())

# Remove numbering from movie names (e.g., "1. Abigail")
df["Movie Name"] = df["Movie Name"].str.replace(r'^\d+\.\s*', '', regex=True)

# Clean Voting Counts (remove parentheses and convert K to numbers)
def clean_votes(v):
    if pd.isna(v):
        return None
    v = v.replace("(", "").replace(")", "")
    if "K" in v:
        return float(v.replace("K", "")) * 1000
    if "M" in v:
        return float(v.replace("M", "")) * 1000000
    return float(v)

df["Voting Counts"] = df["Voting Counts"].apply(clean_votes)

# Convert ratings
df["Ratings"] = pd.to_numeric(df["Ratings"], errors="coerce")

# Duration is currently showing year; keep it but convert to number
df["Duration"] = pd.to_numeric(df["Duration"], errors="coerce")

# Replace missing genre with "Unknown"
df["Genre"] = df["Genre"].fillna("Unknown")

# Remove rows with missing movie name
df = df.dropna(subset=["Movie Name"])

# Save cleaned data
df.to_csv("data/clean_movies.csv", index=False)

print("\nCleaning completed")
print(df.head())
print("\nRows after cleaning:", len(df))