from datetime import datetime
import os
from dotenv import load_dotenv
from google.cloud import bigquery
import pandas

from app import APP_NAME, APP_ENV, STORAGE_ENV
from app.datetime_decorator import parse_timestamp

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TOPICS_CSV_FILEPATH = os.path.join(DATA_DIR, "topics.csv")
TWEETS_CSV_FILEPATH = os.path.join(DATA_DIR, "tweets.csv")

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # implicit check by google.cloud (and keras)
BQ_PROJECT_NAME = os.getenv("BQ_PROJECT_NAME", default="tweet-collector-py")
BQ_DATASET_NAME = os.getenv("BQ_DATASET_NAME", default=f"{APP_NAME}_{APP_ENV}") #> "impeachment_production"

def topic_seeds(csv_filepath=TOPICS_CSV_FILEPATH):
    """Returns a list of topic strings from the local topics CSV file"""
    topics_df = pandas.read_csv(csv_filepath)
    topics = topics_df["topic"].tolist()
    return topics

def append_topics_to_csv(topics, csv_filepath=TOPICS_CSV_FILEPATH):
    """Param: topics (list<str>) like ['topic1', 'topic 2']"""
    column_names = ['topic']
    new_df = pandas.DataFrame(topics, columns=column_names)
    if os.path.isfile(csv_filepath):
        new_df.to_csv(csv_filepath, mode="a", header=False, index=False)
    else:
        new_df.to_csv(csv_filepath, index=False)

def append_tweets_to_csv(tweets, csv_filepath=TWEETS_CSV_FILEPATH):
    """Param: tweets (list<dict>)"""
    column_names = [
        'status_id', 'status_text', 'truncated', 'retweet_status_id', 'reply_status_id', 'reply_user_id', 'is_quote', 'geo', 'created_at',
        'user_id', 'user_name', 'user_screen_name', 'user_description', 'user_location', 'user_verified', 'user_created_at'
    ]
    #column_names = list(tweets[0].keys())
    #print("COLUMN NAMES", column_names)
    new_df = pandas.DataFrame(tweets, columns=column_names)
    if os.path.isfile(csv_filepath):
        new_df.to_csv(csv_filepath, mode="a", header=False, index=False)
    else:
        new_df.to_csv(csv_filepath, index=False)

class BigQueryService():
    def __init__(self, project_name=BQ_PROJECT_NAME, dataset_name=BQ_DATASET_NAME):
        self.client = bigquery.Client()
        self.project_name = project_name
        self.dataset_name = dataset_name #> "impeachment_production", "impeachment_test", etc.
        self.dataset_ref = self.client.dataset(self.dataset_name)
        self.dataset_address = f"{self.project_name}.{self.dataset_name}"
        print("BQ SERVICE:", self.dataset_address.upper())

        self.tweets_table_name = "tweets"
        self.tweets_table_ref = self.dataset_ref.table(self.tweets_table_name)
        self.tweets_table = self.client.get_table(self.tweets_table_ref) # an API call (caches results for subsequent inserts)
        self.tweets_table_address = f"{self.dataset_address}.{self.tweets_table_name}"

        self.topics_table_name = "topics"
        self.topics_table_ref = self.dataset_ref.table(self.topics_table_name)
        self.topics_table = self.client.get_table(self.topics_table_ref) # an API call (caches results for subsequent inserts)
        self.topics_table_address = f"{self.dataset_address}.{self.topics_table_name}"

    def append_tweets(self, tweets):
        """Param: tweets (list<dict>)"""
        rows_to_insert = [list(twt.values()) for twt in tweets]
        errors = self.client.insert_rows(self.tweets_table, rows_to_insert)
        return errors

    def fetch_topics(self):
        """Returns a list of table rows"""
        sql = f"""
            SELECT topic, created_at
            FROM `{self.topics_table_address}`
            ORDER BY created_at;
        """
        results = self.execute_query(sql)
        return list(results)

    def append_topics(self, topics):
        """
        Inserts topics unless they already exist
        Param: topics (list<dict>)
        """
        rows = self.fetch_topics()
        existing_topics = [row.topic for row in rows]
        new_topics = [topic for topic in topics if topic not in existing_topics]
        if new_topics:
            created_at = parse_timestamp(datetime.now())
            rows_to_insert = [[new_topic, created_at] for new_topic in new_topics]
            errors = self.client.insert_rows(self.topics_table, rows_to_insert)
            return errors
        else:
            print("NO NEW TOPICS...")
            return []

    def execute_query(self, sql):
        """Param: sql (str)"""
        job = self.client.query(sql)
        return job.result()

if __name__ == "__main__":

    if STORAGE_ENV == "remote":
        from conftest import tweet_attributes, retweet_attributes

        bq_service = BigQueryService()

        print("--------------------")
        print("IDEPOTENTLY SEEDING TOPICS...")
        topics = topic_seeds()
        bq_service.append_topics(topics)

        print("--------------------")
        print("FETCHING TOPICS...")
        results = bq_service.fetch_topics()
        for row in results:
            print(row)
            print("---")

        exit()

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

    else:
        print("THERE'S NOTHING GOING ON HERE WITH LOCAL STORAGE YET...")
