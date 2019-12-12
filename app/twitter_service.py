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
    """Param status (tweepy.models.Status)"""
    user = status.user

    row = {
        "status_id": status.id_str,
        "status_text": remove_line_breaks(status.text)
        #"full_text": parse_full_text(status),
        "status_geo": status.geo,
        "status_created_at": timestamp(status.created_at),

        "user_id": user.id_str,
        "user_screen_name": user.screen_name,
        "user_description": remove_line_breaks(user.description),
        "user_location": user.location,
        "user_verified": user.verified,
    }
    return row

def timestamp(my_dt):
    """
    Param my_dt (datetime.datetime) like status.created_at
    Converts datetime to string, formatted for Google BigQuery as YYYY-MM-DD HH:MM[:SS[.SSSSSS]]
    """
    return my_dt.strftime("%Y-%m-%d %H:%M:%S")

def remove_line_breaks(my_str):
    """
    Removes line-breaks for cleaner storage
    Param my_str (str)
    """
    description = user_attrs["description"]
    # handle null user descriptions
    if my_str:
        my_str = my_str.replace("\n"," ")
    return my_str

def parse_full_text(status):
    """Param status (tweepy.models.Status)"""
    # GET FULL TEXT (THIS SHOULD BE EASIER)
    # h/t: https://github.com/tweepy/tweepy/issues/974#issuecomment-383846209

    if hasattr(status, "retweeted_status"):
        sts = status.retweeted_status
    else:
        sts = status

    if hasattr(sts, "full_text"):
        full_text = sts.full_text
    elif hasattr(sts, "extended_tweet"):
        full_text = sts.extended_tweet["full_text"]
    else:
        full_text = sts.text

    full_text = full_text.replace("\n"," ") # remove line breaks for cleaner storage
    #print(status.id_str, status.user.screen_name.upper(), "says:", full_text)

    return full_text

if __name__ == "__main__":
    api = twitter_api()
    print("API", type(api))

    status = api.get_status(1201308452850675712, tweet_mode="extended")
    print("STATUS", type(status))
    pprint(status._json)

    #breakpoint()
