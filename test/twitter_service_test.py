from tweepy.auth import OAuthHandler
from tweepy.api import API
from tweepy.models import Status

from app.twitter_service import twitter_api, parse_status, parse_string, parse_timestamp
from conftest import parsed_tweet, parsed_retweet

def test_twitter_api():
    api = twitter_api()
    assert isinstance(api, API)
    assert isinstance(api.auth, OAuthHandler)
    assert "get_status" in dir(api)

def test_get_status(tweet, retweet):
    assert isinstance(tweet, Status)
    assert isinstance(retweet, Status)

def test_parse_status(tweet, retweet, parsed_tweet, parsed_retweet):
    assert parse_status(tweet) == parsed_tweet
    assert parse_status(retweet) == parsed_retweet

def test_parse_string():
    assert parse_string("  Hello \n World  ") == "Hello   World"
    assert parse_string(None) == None

def test_parse_timestamp(tweet):
    assert parse_timestamp(tweet.created_at) == '2019-12-02 01:13:49'
    assert parse_timestamp(tweet.user.created_at) == '2010-05-26 23:17:10'
