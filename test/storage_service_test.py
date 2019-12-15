import os
import pandas

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

#print("BQ CLIENT", type(client)) #> <class 'google.cloud.bigquery.client.Client'>
#print("RESULTS", type(results)) #>  <class 'google.cloud.bigquery.table.RowIterator'>
#print("ROW", type(row)) #> <class 'google.cloud.bigquery.table.Row'>

def test_bq_tweet_collection(bq_service, parsed_tweet, parsed_retweet):
    errors = bq_service.append_tweets([parsed_tweet, parsed_retweet])
    assert errors == []

def test_bq_topic_addition(bq_service):
    errors = bq_service.add_topic("#MyNewTopic")
    assert errors == []
