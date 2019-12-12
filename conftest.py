
import pytest

from app import tweet_attributes, retweet_attributes
from app.twitter_service import twitter_api as api

@pytest.fixture(scope="module")
def twitter_api():
    return api()

@pytest.fixture(scope="module")
def tweet(twitter_api):
    """mimics the data returned by the listener's on_status() method"""
    return twitter_api.get_status(1201308452850675712)

@pytest.fixture(scope="module")
def tweet_ext(twitter_api):
    """extended mode gets more data than the listener's on_status method"""
    return twitter_api.get_status(1201308452850675712, tweet_mode="extended")

@pytest.fixture(scope="module")
def retweet(twitter_api):
    """mimics the data returned by the listener's on_status() method"""
    return twitter_api.get_status(1201341021432365056)

@pytest.fixture(scope="module")
def retweet_ext(twitter_api):
    """extended mode gets more data than the listener's on_status method"""
    return twitter_api.get_status(1201341021432365056, tweet_mode="extended")

#@pytest.fixture(scope="module")
#def tweet_with_weird_user_description_1(twitter_api):
#    return twitter_api.get_status(1205017687216336896)
#
#@pytest.fixture(scope="module")
#def tweet_with_weird_user_description_2(twitter_api):
#    return twitter_api.get_status(1205017997162606594)

@pytest.fixture()
def parsed_tweet():
    return tweet_attributes

@pytest.fixture()
def parsed_retweet():
    return retweet_attributes
