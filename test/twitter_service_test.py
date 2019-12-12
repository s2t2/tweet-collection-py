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

#def test_parse_string(tweet_with_weird_user_description_1, tweet_with_weird_user_description_2):
def test_parse_string():
    assert parse_string("  Hello \n World  ") == "Hello   World"
    assert parse_string(None) == None

    #s1 = tweet_with_weird_user_description_1
    #assert parse_string(s1.text) == 'IMPEACH!! SONKO must be impeached  and Nairobi heads to polls. Uhuru should FRONT PETER KENNETH &amp; Raila a lady depu… https://t.co/KnRauPWfta'
    parsed_user_description = '“Occasionally the tree of Liberty must be watered with the blood of Patriots and Tyrants.”  ― Thomas Jefferson'
    #assert parse_string(s1.user.description) == parsed_user_description
    assert parse_string('“Occasionally the tree of Liberty must be watered with the blood of Patriots and Tyrants.”\r\n― Thomas Jefferson') == parsed_user_description

    #s2 = tweet_with_weird_user_description_2
    #assert parse_string(s2.text) == 'RT @QasimRashid: 45’s supporters in Pennsylvania threaten mass violence &amp; civil war if 45 is impeached 😳  This is utterly horrifying &amp; a re…'
    parsed_user_description = 'Sunshine with a bit of Hurricane .. Prince4ever...  Happily single in Seattle...  Fan of ALL Seattle teams... $piratesunshine'
    #assert parse_string(s2.user.description) == parsed_user_description
    assert parse_string('Sunshine with a bit of Hurricane ..\nPrince4ever...\r\nHappily single in Seattle...\r\nFan of ALL Seattle teams...\n$piratesunshine') == parsed_user_description

def test_parse_timestamp(tweet):
    assert parse_timestamp(tweet.created_at) == '2019-12-02 01:13:49'
    assert parse_timestamp(tweet.user.created_at) == '2010-05-26 23:17:10'
