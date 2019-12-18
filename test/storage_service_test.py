import os
import pandas
from google.cloud.bigquery.client import Client
from google.cloud.bigquery.table import RowIterator, Row

from app.storage_service import local_topics, append_tweets_to_csv, append_topics_to_csv, BigQueryService

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def test_local_topics():
    topics = local_topics(os.path.join(DATA_DIR, "mock_topics.csv"))
    assert sorted(topics) == ["#HelloWorld", "my mock topic"]

def test_csv_topic_additions():
    TOPICS_CSV_FILEPATH = os.path.join(DATA_DIR, "temp_topics.csv")

    if os.path.isfile(TOPICS_CSV_FILEPATH):
        os.remove(TOPICS_CSV_FILEPATH)
    assert not os.path.isfile(TOPICS_CSV_FILEPATH)

    # when the local CSV file doesn't yet exist (first rows):
    append_topics_to_csv(["local topic 1", "local topic 2"], csv_filepath=TOPICS_CSV_FILEPATH)
    assert os.path.isfile(TOPICS_CSV_FILEPATH)
    topics_df = pandas.read_csv(TOPICS_CSV_FILEPATH)
    #assert topics_df.columns.tolist() == ["topic"]
    #assert len(topics_df) == 2
    assert topics_df["topic"].tolist() == ["local topic 1", "local topic 2"]

    # after the local CSV file already exists (subsequent rows):
    append_topics_to_csv(["local topic 3", "local topic 1"], csv_filepath=TOPICS_CSV_FILEPATH)
    # it should only insert topics if they don't already exist
    appended_topics_df = pandas.read_csv(TOPICS_CSV_FILEPATH)
    #print(appended_topics_df.head())
    #assert topics_df.columns.tolist() == ["topic"]
    #assert len(appended_topics_df) == 3
    assert appended_topics_df["topic"].tolist() == ["local topic 1", "local topic 2", "local topic 3"]

def test_csv_tweet_collection(parsed_tweet, parsed_retweet):
    TWEETS_CSV_FILEPATH = os.path.join(DATA_DIR, "temp_tweets.csv")

    if os.path.isfile(TWEETS_CSV_FILEPATH):
        os.remove(TWEETS_CSV_FILEPATH)

    # when the local CSV file doesn't yet exist (first rows):
    append_tweets_to_csv([parsed_tweet, parsed_retweet], csv_filepath=TWEETS_CSV_FILEPATH)
    assert os.path.isfile(TWEETS_CSV_FILEPATH)
    tweets_df = pandas.read_csv(TWEETS_CSV_FILEPATH)
    assert len(tweets_df) == 2

    # after the local CSV file already exists (subsequent rows):
    append_tweets_to_csv([parsed_tweet, parsed_retweet], csv_filepath=TWEETS_CSV_FILEPATH)
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
    assert isinstance(results, list) #assert isinstance(results, RowIterator)
    assert isinstance(results[0], Row)
    topics = [row.topic for row in results]
    assert sorted(topics) == ['#MyNewTopic', 'Another Topic']

def test_bq_append_topics(bq_service):
    errors = bq_service.append_topics(["#MyNewTopic", "Another Topic"])
    assert errors == []
