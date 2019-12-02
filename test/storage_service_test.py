import os
import pandas

from app.storage_service import collect

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_TWEETS_FILEPATH = os.path.join(TEST_DATA_DIR, "tweets.csv")
TEST_USERS_FILEPATH = os.path.join(TEST_DATA_DIR, "users.csv")

def test_collection():

    if os.path.isfile(TEST_TWEETS_FILEPATH):
        os.remove(TEST_TWEETS_FILEPATH)
    if os.path.isfile(TEST_USERS_FILEPATH):
        os.remove(TEST_USERS_FILEPATH)

    tweet = {
        'id_str': '1201316965991799999',
        'created_at': 'Mon Dec 02 01:47:38 +0000 2019',
        'geo': None,
        'full_text': 'RT @OtherUser: There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office. \n\nBut there are still 3 rea…'
    }
    user = {
        'id_str': '18199999',
        'screen_name': 'User123',
        'description': 'Some profile content here.',
        'utc_offset': None,
        'location': 'NYC/Rockland County/Cape Cod ',
        'verified': True
    }

    result = collect(tweet, user, tweets_filepath=TEST_TWEETS_FILEPATH, users_filepath=TEST_USERS_FILEPATH)

    assert os.path.isfile(TEST_TWEETS_FILEPATH)
    assert os.path.isfile(TEST_USERS_FILEPATH)

    tweets_df = pandas.read_csv(TEST_TWEETS_FILEPATH)
    users_df = pandas.read_csv(TEST_TWEETS_FILEPATH)
