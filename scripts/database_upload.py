import pandas as pd
from sqlalchemy import create_engine

# Load cleaned dataset
df = pd.read_csv("data/clean_movies.csv")

# Create MySQL connection
engine = create_engine("mysql+pymysql://root@localhost/imdb_db")

# Upload dataset to MySQL table
df.to_sql("movies", engine, if_exists="replace", index=False)

print("Dataset successfully uploaded to MySQL!")
print("Rows inserted:", len(df))