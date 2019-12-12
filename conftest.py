
import pytest

from app.twitter_service import twitter_api as api

#
# TWITTER SERVICE
#

@pytest.fixture(scope="module")
def twitter_api():
    return api()

@pytest.fixture(scope="module")
def tweet(twitter_api):
    """mimics the data returned by the listener's on_status() method"""
    status = twitter_api.get_status(1201308452850675712)
    print("TWEET:")
    print(status._json)
    return status

@pytest.fixture(scope="module")
def tweet_ext(twitter_api):
    """extended mode gets more data than the listener's on_status method"""
    status = twitter_api.get_status(1201308452850675712, tweet_mode="extended")
    print("TWEET EXT:")
    print(status._json)
    return status

@pytest.fixture(scope="module")
def retweet(twitter_api):
    """mimics the data returned by the listener's on_status() method"""
    status = twitter_api.get_status(1201341021432365056)
    print("TWEET EXT:")
    print(status._json)
    return status

@pytest.fixture(scope="module")
def retweet_ext(twitter_api):
    """extended mode gets more data than the listener's on_status method"""
    return twitter_api.get_status(1201341021432365056, tweet_mode="extended")

#
# STORAGE SERVICE
#

@pytest.fixture()
def collected_tweet_attributes():
    return {
        'id_str': '12345',
        'full_text': 'My collected tweet',
        'geo': None,
        'created_at': '2019-12-02 01:13:49',
        'user_id_str': '98776655443',
        'user_screen_name': 'user123',
        'user_description': 'Testing the storage service',
        'user_location': '',
        'user_verified': False
    }
