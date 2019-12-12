from tweepy.auth import OAuthHandler
from tweepy.api import API
from tweepy.models import Status

from app.twitter_service import twitter_api, parse_status, parse_string, parse_timestamp

def test_twitter_api():
    api = twitter_api()
    assert isinstance(api, API)
    assert isinstance(api.auth, OAuthHandler)
    assert "get_status" in dir(api)

def test_get_status(tweet, retweet):
    assert isinstance(tweet, Status)
    assert isinstance(retweet, Status)

def test_parse_status(tweet, retweet):
    assert parse_status(tweet) == {
        'status_id': '1201308452850675712',
        'retweet_of_status_id': None,
        'in_reply_to_status_id': None,
        'in_reply_to_user_id': None,
        'text': 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are… https://t.co/uHrShOKq8f',
        'truncated': True,
        'geo': None,
        'created_at': '2019-12-02 01:13:49',
        'user_id': '148529707',
        'user_name': 'Robert Reich',
        'user_screen_name': 'RBReich',
        'user_description': 'Berkeley prof, former Sec. of Lab. @InequalityMedia. Movies "Saving Capitalism" & "Inequality for All" on Netflix. Books: The Common Good, Saving Capitalism,etc',
        'user_location': 'Berkeley, CA',
        'user_verified': True,
        'user_created_at': '2010-05-26 23:17:10'
    }
    assert parse_status(retweet) == {
        'status_id': '1201341021432365056',
        'retweet_of_status_id': None, # 1201308452850675712
        'in_reply_to_status_id': None,
        'in_reply_to_user_id': None,
        'text': 'RT @RBReich: There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 rea…',
        'truncated': False,
        'geo': None,
        'created_at': '2019-12-02 03:23:14',
        'user_id': '1188953381152231425',
        'user_name': 'Donald Olson',
        'user_screen_name': 'DonaldO36048407',
        'user_description': 'You tell me what you think , I will tell you what I think . If we agree fine , If not fine , lets keep talking !',
        'user_location': '',
        'user_verified': False,
        'user_created_at': '2019-10-28 23:00:46'
    }

def test_parse_string():
    assert parse_string("  Hello \n World  ") == "Hello   World"

def test_parse_timestamp(tweet):
    assert parse_timestamp(tweet.created_at) == '2019-12-02 01:13:49'
    assert parse_timestamp(tweet.user.created_at) == '2010-05-26 23:17:10'
