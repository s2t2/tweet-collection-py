from pprint import pprint

from app.tweet_collector import (TweetCollector, backoff_strategy,
    is_collectable, parse_timestamp, parse_status, parse_full_text)

def test_backoff_strategy():
    assert backoff_strategy(2) == 9
    assert backoff_strategy(7) == 64

def test_is_collectable(tweet, retweet):
    breakpoint()
    assert is_collectable(tweet) == True
    assert is_collectable(retweet) == True

def test_parse_timestamp(tweet, retweet):
    assert parse_timestamp(tweet) == "2019-12-02 04:29:13"
    assert parse_timestamp(retweet) == "2019-12-02 04:29:13"

def test_parsing_methods(tweet, tweet_ext, retweet, retweet_ext):

    listener = TweetCollector()

    TWEET_TEXT = 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless. https://t.co/y60SDLGekb'

    # ORIGINAL TWEET

    #tweet = listener.api.get_status(1201308452850675712)
    assert hasattr(tweet, "retweeted_status") == False
    assert is_collectable(tweet) == True
    assert parse_full_text(tweet) == TWEET_TEXT
    assert parse_status(tweet) == {
        'status_id': '1201308452850675712',
        'rt_status_id': None,
        'full_text': 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless. https://t.co/y60SDLGekb',
        'geo': None,
        'created_at': '2019-12-02 01:13:49',
        'user_id_str': '148529707',
        'user_screen_name': 'RBReich',
        'user_description': 'Berkeley prof, former Sec. of Lab. @InequalityMedia. Movies "Saving Capitalism" & "Inequality for All" on Netflix. Books: The Common Good, Saving Capitalism,etc',
        'user_location': 'Berkeley, CA',
        'user_verified': True
    }

    #tweet_ext = listener.api.get_status(1201308452850675712, tweet_mode="extended")
    assert hasattr(tweet_ext, "retweeted_status") == False
    assert is_collectable(tweet_ext) == True
    assert parse_full_text(tweet_ext) == TWEET_TEXT
    assert parse_status(tweet_ext) == {
        'status_id': '1201308452850675712',
        'rt_status_id': None,
        'full_text': 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless. https://t.co/y60SDLGekb',
        'geo': None,
        'created_at': '2019-12-02 01:13:49',
        'user_id_str': '148529707',
        'user_screen_name': 'RBReich',
        'user_description': 'Berkeley prof, former Sec. of Lab. @InequalityMedia. Movies "Saving Capitalism" & "Inequality for All" on Netflix. Books: The Common Good, Saving Capitalism,etc',
        'user_location': 'Berkeley, CA',
        'user_verified': True
    }

    exit()

    # RETWEET

    #retweet = listener.api.get_status(1201341021432365056)
    assert hasattr(retweet, "retweeted_status") == True
    assert is_collectable(retweet) == True
    assert parse_full_text(retweet) == 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are… https://t.co/uHrShOKq8f' # TODO: get original text for these retweets as well! or continue to filter them out
    assert parse_status(retweet) == {
        'status_id': '1201341021432365056',
        'rt_status_id': tweet.id_str, #'1201308452850675712', # the tweet
        'full_text': 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless. https://t.co/y60SDLGekb',
        'geo': None,
        'created_at': '2019-12-02 01:13:49',
        'user_id_str': '148529707',
        'user_screen_name': '____',
        'user_description': '______',
        'user_location': '___',
        'user_verified': False
    }

    #retweet_ext = listener.api.get_status(1201341021432365056, tweet_mode="extended")
    assert hasattr(retweet_ext, "retweeted_status") == True
    assert is_collectable(retweet_ext) == False
    assert parse_full_text(retweet_ext) == TWEET_TEXT
    assert parse_status(retweet_ext) == {
        'id_str': '1201341021432365056',
        'rt_id_str': '1201308452850675712',
        'full_text': 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless. https://t.co/y60SDLGekb',
        'geo': None,
        'created_at': '2019-12-02 01:13:49',
        'user_id_str': '148529707',
        'user_screen_name': '____',
        'user_description': '______',
        'user_location': '___',
        'user_verified': False
    }
