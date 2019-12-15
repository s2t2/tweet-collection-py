import os
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas

from app import APP_NAME, APP_ENV

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TWEETS_CSV_FILEPATH = os.path.join(DATA_DIR, "tweets.csv")

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # implicit check by google.cloud (and keras)
BQ_PROJECT_NAME = os.getenv("BQ_PROJECT_NAME", default="tweet-collector-py")
BQ_DATASET_NAME = os.getenv("BQ_DATASET_NAME", default=f"{APP_NAME}_{APP_ENV}") #> "impeachment_production"
BQ_TABLE_NAME = os.getenv("BQ_TABLE_NAME", default="tweets")

def append_to_csv(tweets, tweets_filepath=TWEETS_CSV_FILEPATH):
    """Param: tweets (list<dict>)"""
    column_names = [
        'status_id', 'status_text', 'truncated', 'retweet_status_id', 'reply_status_id', 'reply_user_id', 'is_quote', 'geo', 'created_at',
        'user_id', 'user_name', 'user_screen_name', 'user_description', 'user_location', 'user_verified', 'user_created_at'
    ]
    #column_names = list(tweets[0].keys())
    #print("COLUMN NAMES", column_names)
    new_df = pandas.DataFrame(tweets, columns=column_names)
    if os.path.isfile(tweets_filepath):
        new_df.to_csv(tweets_filepath, mode="a", header=False, index=False)
    else:
        new_df.to_csv(tweets_filepath, index=False)

class BigQueryService():
    def __init__(self, project_name=BQ_PROJECT_NAME, dataset_name=BQ_DATASET_NAME, table_name=BQ_TABLE_NAME):
        self.client = bigquery.Client()
        self.project_name = project_name
        self.dataset_name = dataset_name #> "impeachment_production", "impeachment_test", etc.
        self.dataset_address = f"{self.project_name}.{self.dataset_name}"
        self.dataset_ref = self.client.dataset(self.dataset_name)

        self.tweets_table_name = "tweets"
        self.tweets_table_address = f"{self.dataset_address}.{self.tweets_table_name}"
        self.tweets_table_ref = self.dataset_ref.table(self.tweets_table_name)
        self.tweets_table = self.client.get_table(self.tweets_table_ref) # an API call (caches results for subsequent inserts)

        self.topics_table_name = "topics"
        self.topics_table_address = f"{self.dataset_address}.{self.topics_table_name}"
        self.topics_table_ref = self.dataset_ref.table(self.topics_table_name)
        self.topics_table = self.client.get_table(self.topics_table_ref) # an API call (caches results for subsequent inserts)

    def append_tweets(self, tweets):
        """Param: tweets (list<dict>)"""
        rows_to_insert = [list(twt.values()) for twt in tweets]
        errors = self.client.insert_rows(self.tweets_table, rows_to_insert)
        return errors

    def add_topic(self, new_topic):
        """Param: topic (str)"""
        rows_to_insert = [[new_topic]]
        errors = self.client.insert_rows(self.topics_table, rows_to_insert)
        return errors

    def execute_query(self, sql):
        """Param: sql (str)"""
        job = self.client.query(sql)
        return job.result()

if __name__ == "__main__":

    from conftest import tweet_attributes, retweet_attributes

    print("BIGQUERY SERVICE...")
    bq_service = BigQueryService()
    print("DATASET ADDRESS:", bq_service.dataset_address.upper())

    print("--------------------")
    print("INSERTING TWEETS...")
    print(tweet_attributes)
    print(retweet_attributes)
    errors = bq_service.append_tweets([tweet_attributes, retweet_attributes])
    print("ERRORS:", errors)

    print("--------------------")
    print("COUNTING TWEETS...")
    sql = f"SELECT count(distinct status_id) as tweets_count FROM `{bq_service.tweets_table_address}`"
    results = bq_service.execute_query(sql)
    print(list(results)[0].tweets_count)

    print("--------------------")
    print("FETCHING LATEST TWEETS...")
    sql = f"""
        SELECT
            status_id, status_text, geo, created_at,
            user_id, user_screen_name, user_description, user_location, user_verified
        FROM `{bq_service.tweets_table_address}`
        ORDER BY created_at DESC
        LIMIT 3
    """
    results = bq_service.execute_query(sql)
    for row in results:
        print(row)
        print("---")

    print("--------------------")
    print("FETCHING TOPICS...")
    sql = f"""
        SELECT topic, created_at
        FROM `{bq_service.topics_table_address}`
    """
    results = bq_service.execute_query(sql)
    for row in results:
        print(row)
        print("---")
