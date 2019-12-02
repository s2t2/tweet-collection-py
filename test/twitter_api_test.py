from pprint import pprint

from app.tweet_collector import TweetCollector, parse_full_text, is_collectable

def test_get_status():
    ORIGINAL_TEXT = 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless. https://t.co/y60SDLGekb'

    listener = TweetCollector()

    # an original tweet:
    status = listener.api.get_status(1201308452850675712, tweet_mode="extended")
    assert hasattr(status, "retweeted_status") == False
    assert is_collectable(status) == True
    assert parse_full_text(status) == ORIGINAL_TEXT

    # a retweet:
    rt_status = listener.api.get_status(1201341021432365056, tweet_mode="extended")
    assert hasattr(rt_status, "retweeted_status")
    assert is_collectable(rt_status) == False
    assert parse_full_text(rt_status) == ORIGINAL_TEXT

     # a retweet (without extended mode, mimics the listener):
    fml_status = listener.api.get_status(1201341021432365056)
    assert hasattr(fml_status, "retweeted_status")
    assert is_collectable(fml_status) == False
    assert parse_full_text(fml_status) == 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are… https://t.co/uHrShOKq8f' # TODO: get original text for these retweets as well! or continue to filter them out

    my_status = listener.api.get_status(1201357629928411136)
    assert is_collectable(my_status) == True
