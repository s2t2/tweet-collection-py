from tweepy.auth import OAuthHandler
from tweepy.api import API
from app.twitter_service import twitter_api

def test_twitter_api():
    api = twitter_api()
    assert isinstance(api, API)
    assert isinstance(api.auth, OAuthHandler)
    assert "get_status" in dir(api)
