from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://www.imdb.com/chart/top/"
driver.get(url)

time.sleep(5)

movies = []
genres = []
ratings = []
votes = []
durations = []

rows = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

print("Movies found:", len(rows))

for row in rows:

    # Movie Name
    try:
        name = row.find_element(By.CSS_SELECTOR, "h3").text
    except:
        name = "Unknown"

    # Rating
    try:
        rating = row.find_element(By.CSS_SELECTOR, ".ipc-rating-star--rating").text
    except:
        rating = "0"

    # Votes
    try:
        vote = row.find_element(By.CSS_SELECTOR, ".ipc-rating-star--voteCount").text
    except:
        vote = "0"

    # Duration
    try:
        metadata = row.find_elements(By.CSS_SELECTOR, ".cli-title-metadata-item")
        duration = metadata[1].text
    except:
        duration = "0"

    # Genre (open movie page)
    try:
        link = row.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(2)

        genre_elements = driver.find_elements(By.CSS_SELECTOR, ".ipc-chip__text")
        genre_list = [g.text for g in genre_elements]

        genre = ", ".join(genre_list)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except:
        genre = "Unknown"

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

df.to_csv("data/imdb_movies.csv", index=False)

print("Dataset saved successfully")