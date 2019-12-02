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
        if os.path.isfile(tweets_filepath):
            tweets_df = pandas.read_csv(tweets_filepath)
            tweets_df.append(tweet, ignore_index=True)
            tweets_df.to_csv(tweets_filepath, mode="a", header=False)
        else:
            #tweet_cols = list(tweet.keys())
            tweets_df = pandas.DataFrame([tweet])
            tweets_df.index.rename("id", inplace=True) # assigns a column label "id" for the index column
            tweets_df.index += 1 # starts indices at one instead of zero
            tweets_df.to_csv(tweets_filepath)

    elif APP_ENV == "production":
        print("SAVING TO BIG QUERY")

#def collect_local():
#    pass
#
#def collect_remote():
#    pass

if __name__ == "__main__":
    print("STORAGE SERVICE...")

    client = storage.Client()

    breakpoint()
