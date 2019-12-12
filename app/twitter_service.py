import os
from pprint import pprint
from dotenv import load_dotenv
import tweepy

load_dotenv()

CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY", default="OOPS")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET", default="OOPS")
ACCESS_KEY = os.getenv("TWITTER_ACCESS_TOKEN", default="OOPS")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", default="OOPS")

def twitter_api():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def parse_status(status):
    """
    Param status (tweepy.models.Status)
    Converts a nested status structure into a flat row of non-normalized status and user attributes
    """

    if hasattr(status, "retweeted_status"):
        retweet_of_status_id_str = status.retweeted_status.id_str
    else:
        retweet_of_status_id_str = None

    user = status.user

    row = {
        "status_id": status.id_str,
        "status_text": parse_string(parse_full_text(status)),
        "truncated": status.truncated,
        "retweet_status_id": retweet_of_status_id_str,
        "reply_status_id": status.in_reply_to_status_id_str,
        "reply_user_id": status.in_reply_to_user_id_str,
        "is_quote": status.is_quote_status,
        "geo": status.geo,
        #"retweet_count": status.retweet_count,
        #"favorite_count": status.favorite_count,
        "created_at": parse_timestamp(status.created_at),

        "user_id": user.id_str,
        "user_name": user.name,
        "user_screen_name": user.screen_name,
        "user_description": parse_string(user.description),
        "user_location": user.location,
        "user_verified": user.verified,
        "user_created_at": parse_timestamp(user.created_at),
    }
    return row

def parse_timestamp(my_dt):
    """
    Param my_dt (datetime.datetime) like status.created_at
    Converts datetime to string, formatted for Google BigQuery as YYYY-MM-DD HH:MM[:SS[.SSSSSS]]
    """
    return my_dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_string(my_str):
    """
    Param my_str (str)
    Removes line-breaks for cleaner CSV storage
    Handles string or null value
    Returns string or null value
    """
    try:
        my_str = my_str.replace("\n", " ")
        my_str = my_str.replace("\r", " ")
        my_str = my_str.strip()
    except AttributeError as err:
        pass
    return my_str

def parse_full_text(status):
    """Param status (tweepy.models.Status)"""
    # GET FULL TEXT (THIS SHOULD BE EASIER)
    # h/t: https://github.com/tweepy/tweepy/issues/974#issuecomment-383846209
    #
    # commenting this out because we're storing the id of the retweeted_status
    #if hasattr(status, "retweeted_status"):
    #    status = status.retweeted_status

    if hasattr(status, "full_text"):
        full_text = status.full_text
    elif hasattr(status, "extended_tweet"):
        full_text = status.extended_tweet["full_text"]
    else:
        full_text = status.text

    #print(status.id_str, status.user.screen_name.upper(), "says:", full_text)

    return full_text

if __name__ == "__main__":
    api = twitter_api()
    print("API", type(api))

    status = api.get_status(1201308452850675712, tweet_mode="extended")
    print("STATUS", type(status))
    pprint(status._json)


    # breakpoint()
    # parse_full_text(status)
