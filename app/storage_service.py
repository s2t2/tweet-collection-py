import os
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas

from app import APP_ENV

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # implicit check by google.cloud (and keras)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TWEETS_CSV_FILEPATH = os.path.join(DATA_DIR, "tweets.csv")

COLUMNS = [
    "id_str", "user_id_str", "full_text", "geo", "created_at" #, "timestamp_ms" # TWEET
    "user_id_str", "user_screen_name", "user_description", "user_location", "user_verified" # USER
]

def append_to_csv(tweet, tweets_filepath=TWEETS_CSV_FILEPATH):
    if os.path.isfile(tweets_filepath):
        df = pandas.read_csv(tweets_filepath)
        df.append(tweet, ignore_index=True)
        df.to_csv(tweets_filepath, mode="a", header=False, index=False)
    else:
        df = pandas.DataFrame([tweet], columns=COLUMNS)
        df.to_csv(tweets_filepath, index=False)

def append_to_bq(tweet, user):
    print("SAVING TO BIG QUERY... (TODO)")

if __name__ == "__main__":
    print("STORAGE SERVICE...")

    client = storage.Client()

    breakpoint()
