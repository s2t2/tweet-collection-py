from pprint import pprint

from app.tweet_collector import TweetCollector, parse_full_text, is_collectable, parse_status

def test_get_status(my_status, rr_status):
    ORIGINAL_TEXT = 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless. https://t.co/y60SDLGekb'

    listener = TweetCollector()

    # an original tweet:
    #status = listener.api.get_status(1201308452850675712, tweet_mode="extended")
    assert hasattr(rr_status, "retweeted_status") == False
    assert is_collectable(rr_status) == True
    assert parse_full_text(rr_status) == ORIGINAL_TEXT

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

    #my_status = listener.api.get_status(1201357629928411136)
    assert is_collectable(my_status) == True

def test_parse_status(my_status, rr_status):
    my_tweet = parse_status(my_status)
    assert my_tweet == {
        'id_str': '1201357629928411136',
        'full_text': 'Testing new script to collect tweets (not RTs) containing the term: impeach',
        'geo': None,
        'created_at': 'Mon Dec 02 04:29:13 +0000 2019',
        'user_id_str': '985535135956291585',
        'user_screen_name': 'prof_rossetti',
        'user_description': 'an account for experimenting with research and development using the Twitter API. nothing to see here!',
        'user_location': '',
        'user_verified': False
    }

    rr_tweet = parse_status(rr_status)
    assert rr_tweet == {
        'id_str': '1201308452850675712',
        'full_text': 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 reasons to impeach him. A failure by Congress to respond to these abuses would effectively render the constitution meaningless. https://t.co/y60SDLGekb',
        'geo': None,
        'created_at': 'Mon Dec 02 01:13:49 +0000 2019',
        'user_id_str': '148529707',
        'user_screen_name': 'RBReich',
        'user_description': 'Berkeley prof, former Sec. of Lab. @InequalityMedia. Movies "Saving Capitalism" & "Inequality for All" on Netflix. Books: The Common Good, Saving Capitalism,etc',
        'user_location': 'Berkeley, CA',
        'user_verified': True
    }
