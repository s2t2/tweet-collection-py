import os
import pandas
from google.cloud.bigquery.client import Client
from google.cloud.bigquery.table import RowIterator, Row

from app.storage_service import append_to_csv, BigQueryService

def test_csv_tweet_collection(parsed_tweet, parsed_retweet):
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    TWEETS_CSV_FILEPATH = os.path.join(DATA_DIR, "tweets.csv")

    if os.path.isfile(TWEETS_CSV_FILEPATH):
        os.remove(TWEETS_CSV_FILEPATH)

    # when the local CSV file doesn't yet exist (first rows):
    append_to_csv([parsed_tweet, parsed_retweet], tweets_filepath=TWEETS_CSV_FILEPATH)
    assert os.path.isfile(TWEETS_CSV_FILEPATH)
    tweets_df = pandas.read_csv(TWEETS_CSV_FILEPATH)
    assert len(tweets_df) == 2

    # after the local CSV file already exists (subsequent rows):
    append_to_csv([parsed_tweet, parsed_retweet], tweets_filepath=TWEETS_CSV_FILEPATH)
    tweets_df = pandas.read_csv(TWEETS_CSV_FILEPATH)
    assert len(tweets_df) == 4

def test_bq_service(bq_service):
    assert isinstance(bq_service.client, Client)
    assert bq_service.dataset_name == "impeachment_test"

def test_bq_tweet_collection(bq_service, parsed_tweet, parsed_retweet):
    errors = bq_service.append_tweets([parsed_tweet, parsed_retweet])
    assert errors == []

def test_bq_fetch_topics(bq_service):
    results = bq_service.fetch_topics()
    assert isinstance(results, RowIterator)
    assert isinstance(results[0], Row)
    assert results[0].topic == "#MyNewTopic"

def test_bq_append_topics(bq_service):
    errors = bq_service.append_topics(["#MyNewTopic", "Another Topic"])
    assert errors == []
