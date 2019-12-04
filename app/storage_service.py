import os
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas

from app import APP_ENV

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # implicit check by google.cloud (and keras)
BQ_PROJECT_NAME = os.getenv("BQ_PROJECT_NAME", default="my-project")
BQ_DATASET_NAME = os.getenv("BQ_DATASET_NAME", default="my_dataset")
BQ_TABLE_NAME = os.getenv("BQ_TABLE_NAME", default="my_table")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TWEETS_CSV_FILEPATH = os.path.join(DATA_DIR, "tweets.csv")
COLUMNS = ["id_str", "full_text", "geo", "created_at", "user_id_str", "user_screen_name", "user_description", "user_location", "user_verified"]

def append_to_csv(tweet, tweets_filepath=TWEETS_CSV_FILEPATH):
    # consider validating the tweet is a dict with an attribute for each column
    new_df = pandas.DataFrame([tweet], columns=COLUMNS)
    if os.path.isfile(tweets_filepath):
        new_df.to_csv(tweets_filepath, mode="a", header=False, index=False)
    else:
        new_df.to_csv(tweets_filepath, index=False)

def append_to_bq(tweet, user):
    print("SAVING TO BIG QUERY... (TODO)")

if __name__ == "__main__":
    print("STORAGE SERVICE...")

    client = bigquery.Client()
    print("BQ CLIENT", type(client)) #> <class 'google.cloud.bigquery.client.Client'>

    sql = f"""
        SELECT
            id_str, full_text, geo, created_at,
            user_id_str, user_screen_name, user_description, user_location, user_verified
        FROM `{BQ_PROJECT_NAME}.{BQ_DATASET_NAME}.{BQ_TABLE_NAME}`
        LIMIT 10
    """
    print("SQL:", sql)

    job = client.query(sql)
    print("JOB", type(job))
    results = job.result()
    print("RESULTS", type(results)) #>  <class 'google.cloud.bigquery.table.RowIterator'>
    print("NUM ROWS (W/ HEADER):", results.total_rows)

    for row in results:
        #print("ROW", type(row)) #> <class 'google.cloud.bigquery.table.Row'>
        print(row)
        print("---")

    breakpoint()
