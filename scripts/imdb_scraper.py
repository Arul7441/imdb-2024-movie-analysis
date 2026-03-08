from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Start driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://www.imdb.com/search/title/?title_type=feature&year=2024-01-01,2024-12-31"
driver.get(url)

time.sleep(6)

movies = []
genres = []
ratings = []
votes = []
durations = []

cards = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

print("Cards found:", len(cards))

for card in cards:

    try:
        name = card.find_element(By.CSS_SELECTOR, "h3").text
    except:
        name = ""

    try:
        genre = card.find_element(By.CSS_SELECTOR, ".ipc-chip__text").text
    except:
        genre = ""

    try:
        rating = card.find_element(By.CSS_SELECTOR, ".ipc-rating-star--rating").text
    except:
        rating = ""

    try:
        vote = card.find_element(By.CSS_SELECTOR, ".ipc-rating-star--voteCount").text
    except:
        vote = ""

    try:
        duration = card.find_element(By.CSS_SELECTOR, ".dli-title-metadata-item").text
    except:
        duration = ""

    movies.append(name)
    genres.append(genre)
    ratings.append(rating)
    votes.append(vote)
    durations.append(duration)

driver.quit()

df = pd.DataFrame({
    "Movie Name": movies,
    "Genre": genres,
    "Ratings": ratings,
    "Voting Counts": votes,
    "Duration": durations
})

print(df.head())
print("Total movies scraped:", len(df))

df.to_csv("data/imdb_movies.csv", index=False)

print("CSV saved in data folder")