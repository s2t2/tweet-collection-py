from pprint import pprint

from tweepy import Stream

from app.tweet_collector import TweetCollector, backoff_strategy, is_collectable

def test_tweet_collector():
    listener = TweetCollector()
    assert "on_status" in dir(listener)
    assert "collect_in_batches" in dir(listener)

    stream = Stream(listener.auth, listener)
    assert "filter" in dir(stream)

def test_is_collectable(tweet, retweet):
    assert is_collectable(tweet) == True
    assert is_collectable(retweet) == True

def test_backoff_strategy():
    assert backoff_strategy(2) == 9
    assert backoff_strategy(7) == 64
