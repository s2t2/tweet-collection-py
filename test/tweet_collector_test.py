from pprint import pprint

from tweepy import Stream

from app.tweet_collector import TweetCollector, backoff_strategy

def test_tweet_collector(listener):
    assert "on_status" in dir(listener)
    assert "collect_in_batches" in dir(listener)
    #assert listener.topics = ['impeach', 'impeached', 'impeachment', '#TrumpImpeachment', '#ImpeachAndConvict', '#ImpeachAndConvictTrump', '#IGReport', '#SenateHearing', '#IGHearing', '@ImpeachmentTrak']
    #assert listener.dev_handle == '@ImpeachmentTrak'
    #assert listener.admin_handles = ['@me', '@you',]

    stream = Stream(listener.auth, listener)
    assert "filter" in dir(stream)

def test_is_admin_request(listener, tweet, admin_add_topic_tweet):
    assert listener.is_admin_request(tweet) == False
    assert listener.is_admin_request(admin_add_topic_tweet) == True

def test_add_topic_command(listener):
    assert listener.add_topic_command == "@ImpeachmentTrak add topic "

def test_parse_new_topic(listener):
    assert listener.parse_new_topic("This is a tweet about stuff") == None
    assert listener.parse_new_topic("@ImpeachmentTrak This is a tweet about stuff") == None
    assert listener.parse_new_topic("@ImpeachmentTrak add topic ") == None
    assert listener.parse_new_topic("@ImpeachmentTrak add topic #FactsMatter") == "#FactsMatter"
    assert listener.parse_new_topic("@ImpeachmentTrak add topic Two Keywords") == "Two Keywords"

def test_is_collectable(listener, tweet, retweet):
    assert listener.is_collectable(tweet) == True
    assert listener.is_collectable(retweet) == True

def test_backoff_strategy():
    assert backoff_strategy(2) == 9
    assert backoff_strategy(7) == 64
