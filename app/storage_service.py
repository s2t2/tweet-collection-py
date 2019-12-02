import os
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas

from app import APP_ENV

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # implicit check by google.cloud (and keras)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TWEETS_CSV_FILEPATH = os.path.join(DATA_DIR, "tweets.csv")
USERS_CSV_FILEPATH = os.path.join(DATA_DIR, "users.csv")

def collect(tweet, user, tweets_filepath=TWEETS_CSV_FILEPATH, users_filepath=USERS_CSV_FILEPATH):
    if APP_ENV == "development":
        print("SAVING TO CSV")

    elif APP_ENV == "production":
        print("SAVING TO BIG QUERY")

if __name__ == "__main__":
    print("STORAGE SERVICE...")

    client = storage.Client()

    breakpoint()
