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

def append_to_csv(tweets, tweets_filepath=TWEETS_CSV_FILEPATH):
    """Param: tweets (list<dict>)"""
    new_df = pandas.DataFrame(tweets, columns=COLUMNS)
    if os.path.isfile(tweets_filepath):
        new_df.to_csv(tweets_filepath, mode="a", header=False, index=False)
    else:
        new_df.to_csv(tweets_filepath, index=False)

class BigQueryService():
    def __init__(self, table_name=BQ_TABLE_NAME):
        self.client = bigquery.Client()
        dataset_ref = self.client.dataset(BQ_DATASET_NAME)
        table_ref = dataset_ref.table(table_name)
        self.table = self.client.get_table(table_ref) # an API call

    def append_to_bq(self, tweets):
        """Param: tweets (list<dict>)"""
        rows_to_insert = [list(twt.values()) for twt in tweets]
        errors = self.client.insert_rows(self.table, rows_to_insert)
        return errors

    def execute_query(self, sql):
        """Param: sql (str)"""
        job = self.client.query(sql)
        return job.result()

if __name__ == "__main__":
    print("STORAGE SERVICE...")

    bq_service = BigQueryService()

    print("--------------------")
    print("COUNTING RECORDS...")
    sql = f"SELECT count(distinct id_str) as tweets_count FROM `{BQ_PROJECT_NAME}.{BQ_DATASET_NAME}.{BQ_TABLE_NAME}`"
    results = bq_service.execute_query(sql)
    print(list(results)[0].tweets_count)

    print("--------------------")
    print("FETCHING LATEST RECORDS...")
    sql = f"""
        SELECT
            id_str, full_text, geo, created_at,
            user_id_str, user_screen_name, user_description, user_location, user_verified
        FROM `{BQ_PROJECT_NAME}.{BQ_DATASET_NAME}.{BQ_TABLE_NAME}`
        ORDER BY created_at DESC
        LIMIT 3
    """
    results = bq_service.execute_query(sql)
    for row in results:
        print(row)
        print("---")
