import os
import pandas

from app.storage_service import append_to_csv, BigQueryService

def test_csv_collection(parsed_tweet, parsed_retweet):
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

def test_bq_collection(parsed_tweet, parsed_retweet):
    bq_service = BigQueryService(table_name="tweets_test")
    errors = bq_service.append_to_bq([parsed_tweet, parsed_retweet])
    assert errors == []
