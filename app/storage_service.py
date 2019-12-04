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
    def __init__(self):
        self.client = bigquery.Client()
        dataset_ref = self.client.dataset(BQ_DATASET_NAME)
        table_ref = dataset_ref.table(BQ_TABLE_NAME)
        self.table = self.client.get_table(table_ref) # an API call

    def append_to_bq(self, tweets):
        """Param: tweets (list<dict>)"""
        rows_to_insert = [list(twt.values()) for twt in tweets]
        errors = self.client.insert_rows(self.table, rows_to_insert)
        return errors

if __name__ == "__main__":
    print("STORAGE SERVICE...")

    bq_service = BigQueryService()

    print("--------------------")
    print("ADDING A RECORD...")
    new_tweet = {
        'id_str': '12345',
        'full_text': 'Inserting a row',
        'geo': None,
        'created_at': '2019-12-02 01:13:49',
        'user_id_str': '98776655443',
        'user_screen_name': 'user123',
        'user_description': 'Testing the storage service',
        'user_location': '',
        'user_verified': False
    }
    errors = bq_service.append_to_bq([new_tweet])
    print("ERRORS:", errors)

    print("--------------------")
    print("FETCHING RECORDS...")
    client = bq_service.client
    #print("BQ CLIENT", type(client)) #> <class 'google.cloud.bigquery.client.Client'>
    sql = f"""
        SELECT
            id_str, full_text, geo, created_at,
            user_id_str, user_screen_name, user_description, user_location, user_verified
        FROM `{BQ_PROJECT_NAME}.{BQ_DATASET_NAME}.{BQ_TABLE_NAME}`
        ORDER BY created_at DESC
        LIMIT 10
    """
    #print("SQL:", sql)
    job = client.query(sql)
    #print("JOB", type(job))
    results = job.result()
    #print("RESULTS", type(results)) #>  <class 'google.cloud.bigquery.table.RowIterator'>
    print("NUM ROWS:", results.total_rows)
    for row in results:
        #print("ROW", type(row)) #> <class 'google.cloud.bigquery.table.Row'>
        print(row)
        print("---")
