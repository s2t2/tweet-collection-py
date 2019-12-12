import os
import pandas

from app.storage_service import append_to_csv, BigQueryService

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TWEETS_CSV_FILEPATH = os.path.join(DATA_DIR, "tweets.csv")

def test_csv_collection(collected_tweet_attributes):
    if os.path.isfile(TWEETS_CSV_FILEPATH):
        os.remove(TWEETS_CSV_FILEPATH)

    # if the local CSV file doesn't exist:
    append_to_csv([collected_tweet_attributes], tweets_filepath=TWEETS_CSV_FILEPATH)
    assert os.path.isfile(TWEETS_CSV_FILEPATH)
    tweets_df = pandas.read_csv(TWEETS_CSV_FILEPATH)
    assert len(tweets_df) == 1

    # if the local CSV file exists:
    append_to_csv([collected_tweet_attributes], tweets_filepath=TWEETS_CSV_FILEPATH)
    tweets_df = pandas.read_csv(TWEETS_CSV_FILEPATH)
    assert len(tweets_df) == 2

#print("BQ CLIENT", type(client)) #> <class 'google.cloud.bigquery.client.Client'>
#print("RESULTS", type(results)) #>  <class 'google.cloud.bigquery.table.RowIterator'>
#print("ROW", type(row)) #> <class 'google.cloud.bigquery.table.Row'>

def test_bq_collection(collected_tweet_attributes):
    bq_service = BigQueryService(table_name="tweets_test")
    errors = bq_service.append_to_bq([collected_tweet_attributes])
    assert errors == []
