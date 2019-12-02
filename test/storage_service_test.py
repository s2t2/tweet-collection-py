import os
import pandas

from app.storage_service import append_to_csv

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_TWEETS_FILEPATH = os.path.join(TEST_DATA_DIR, "tweets.csv")
TEST_USERS_FILEPATH = os.path.join(TEST_DATA_DIR, "users.csv")

def test_csv_collection():

    if os.path.isfile(TEST_TWEETS_FILEPATH):
        os.remove(TEST_TWEETS_FILEPATH)
    if os.path.isfile(TEST_USERS_FILEPATH):
        os.remove(TEST_USERS_FILEPATH)

    tweet = {
        'id_str': '1201316965991799999',
        'user_id_str': '18199999',
        'full_text': 'RT @OtherUser: There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless.',
        'geo': None,
        'created_at': 'Mon Dec 02 02:58:42 +0000 2019',
        'timestamp_ms': '1575255522770'
    }
    user = {
        'id_str': '18199999',
        'screen_name': 'User123',
        'description': 'Some profile content here.',
        'location': 'NYC/Rockland County/Cape Cod ',
        'verified': True
    }

    # if the local files don't already exist:
    append_to_csv(tweet, user, tweets_filepath=TEST_TWEETS_FILEPATH, users_filepath=TEST_USERS_FILEPATH)
    assert os.path.isfile(TEST_TWEETS_FILEPATH)
    tweets_df = pandas.read_csv(TEST_TWEETS_FILEPATH)
    assert len(tweets_df) == 1

    # if the local files already exist:
    append_to_csv(tweet, user, tweets_filepath=TEST_TWEETS_FILEPATH, users_filepath=TEST_USERS_FILEPATH)
    tweets_df = pandas.read_csv(TEST_TWEETS_FILEPATH)
    assert len(tweets_df) == 2
