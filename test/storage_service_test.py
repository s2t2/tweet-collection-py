import os
import pandas

from app.storage_service import append_to_csv, BigQueryService

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TWEETS_CSV_FILEPATH = os.path.join(DATA_DIR, "tweets.csv")

def test_csv_collection():

    if os.path.isfile(TWEETS_CSV_FILEPATH):
        os.remove(TWEETS_CSV_FILEPATH)

    tweet = {
        'id_str': '1201316965991799999',
        'full_text': 'RT @OtherUser: There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless.',
        'geo': None,
        'created_at': "2019-12-02 01:13:49",
        'user_id_str': '18199999',
        'user_screen_name': 'User123',
        'user_description': 'Some profile content here.',
        'user_location': 'NYC/Rockland County/Cape Cod ',
        'user_verified': True
    }

    # if the local files don't already exist:
    append_to_csv([tweet], tweets_filepath=TWEETS_CSV_FILEPATH)
    assert os.path.isfile(TWEETS_CSV_FILEPATH)
    tweets_df = pandas.read_csv(TWEETS_CSV_FILEPATH)
    assert len(tweets_df) == 1

    # if the local files already exist:
    append_to_csv([tweet], tweets_filepath=TWEETS_CSV_FILEPATH)
    tweets_df = pandas.read_csv(TWEETS_CSV_FILEPATH)
    assert len(tweets_df) == 2

#print("BQ CLIENT", type(client)) #> <class 'google.cloud.bigquery.client.Client'>
#print("RESULTS", type(results)) #>  <class 'google.cloud.bigquery.table.RowIterator'>
#print("ROW", type(row)) #> <class 'google.cloud.bigquery.table.Row'>

def test_bq_collection(mock_tweet):
    bq_service = BigQueryService(table_name="tweets_test")
    errors = bq_service.append_to_bq([mock_tweet])
    assert errors == []
