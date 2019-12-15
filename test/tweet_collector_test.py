from pprint import pprint

from tweepy import Stream

from app.tweet_collector import TweetCollector

def test_tweet_collector(listener):
    assert "on_status" in dir(listener)
    assert "collect_in_batches" in dir(listener)
    assert listener.topics == ['topic1', 'topic2', '#topic3', "#TopicFour"]
    assert listener.dev_handle == '@dev_account'
    assert listener.admin_handles == ['@admin1', '@admin2']

    stream = Stream(listener.auth, listener)
    assert "filter" in dir(stream)

def test_is_admin_request(tweet, admin_add_topic_tweet):
    # use real vars here to accommodate the nature of the admin_add_topic_tweet (because we're testing real tweets)
    real_listener = TweetCollector(dev_handle="@ImpeachmentTrak", admin_handles=["@prof_rossetti"], topics=["topic1", "topic2", "topic3"])
    assert real_listener.is_admin_request(tweet) == False
    assert real_listener.is_admin_request(admin_add_topic_tweet) == True

#def test_process_admin_request(real_listener, tweet, admin_add_topic_tweet):
#    assert real_listener.process_admin_request(tweet) == False
#    assert real_listener.process_admin_request(admin_add_topic_tweet) == True

def test_add_topic_command(listener):
    assert listener.add_topic_command == "@dev_account add topic "

def test_parse_new_topic(listener):
    assert listener.parse_new_topic("This is a tweet about stuff") == None
    assert listener.parse_new_topic("@dev_account This is a tweet about stuff") == None
    assert listener.parse_new_topic("@dev_account add topic ") == None
    assert listener.parse_new_topic("@dev_account add topic #FactsMatter") == "#FactsMatter"
    assert listener.parse_new_topic("@dev_account add topic Two Keywords") == "Two Keywords"

def test_is_collectable(listener, tweet, retweet):
    assert listener.is_collectable(tweet) == True
    assert listener.is_collectable(retweet) == True

def test_backoff_strategy(listener):
    assert listener.backoff_strategy(2) == 9
    assert listener.backoff_strategy(7) == 64
