import os
from pprint import pprint

from tweepy.streaming import StreamListener
from tweepy import Stream

from app import APP_ENV
from app.twitter_service import twitter_api
from app.notification_service import send_email
from app.storage_service import append_to_csv, append_to_bq

TOPICS_LIST = ["impeach", "impeachment"] # todo: dynamically compile list from comma-separated env var string like "topic1,topic2"
# NOTE: "impeachment" keywords don't trigger the "impeach" filter, so adding "impeachment" as well
#TOPICS_LIST = ["impeach -filter:retweets"] # doesn't work

def is_collectable(status):
    return (status.lang == "en"
            #and status.user.verified
            and status.in_reply_to_status_id == None
            and status.in_reply_to_user_id == None
            and status.in_reply_to_screen_name == None
            and status.is_quote_status == False
            and status.retweeted == False
            #and status.retweeted_status == None #> AttributeError: 'Status' object has no attribute 'retweeted_status'
            and not hasattr(status, "retweeted_status")
    )

def parse_full_text(status):
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

def parse_status(status):
    full_text = parse_full_text(status)
    twt = status._json
    usr = twt["user"]

    user_description = usr["description"] # can expect the attribute, but sometimes the value is null
    if user_description:
        user_description = user_description.replace("\n"," ")

    # BQ says... Required format is YYYY-MM-DD HH:MM[:SS[.SSSSSS]];
    #created_at =

    tweet = {
        "id_str": twt["id_str"],
        "full_text": full_text, #> 'Refuse censure! Make them try to impeach and beat it. Mr President you are guilty of no crime. Continue the exposure of these subversives that are so desperate to smear you for draining the swamp!'
        "geo": twt["geo"], #> None or __________
        "created_at": twt["created_at"], #> 'Mon Dec 02 01:06:52 +0000 2019'
        #"timestamp_ms": twt["timestamp_ms"], Not in all tweets WAT?
        "user_id_str": usr["id_str"],
        "user_screen_name": usr["screen_name"],
        "user_description": user_description, # remove line breaks for cleaner storage
        "user_location": usr["location"],
        "user_verified": usr["verified"],
    }

    return tweet

class TweetCollector(StreamListener):

    def __init__(self):
        self.api = twitter_api()
        self.auth = self.api.auth
        self.counter = 0

    def on_status(self, status):
        if is_collectable(status):
            self.counter +=1
            ###if self.counter > 3: raise RuntimeError("OOPS") # UNCOMMENT TO TEST NOTIFICATION EMAILS
            print("----------------")
            print(f"DETECTED AN INCOMING TWEET! ({self.counter} -- {status.id_str})")
            tweet = parse_status(status)
            pprint(tweet)
            if APP_ENV == "development":
                append_to_csv(tweet)
            elif APP_ENV == "production":
                append_to_bq(tweet)

    def on_connect(self):
        print("LISTENER IS CONNECTED!")

    def on_exception(self, exception):
        # has encountered errors:
        #  + urllib3.exceptions.ProtocolError
        #  + urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool
        print("EXCEPTION:", type(exception))
        print(exception)
        contents = f"{type(exception)}<br>{exception}"
        send_email(subject="Tweet Collection - Exception", contents=contents)

    def on_error(self, status_code):
        print("ERROR:", status_code)
        contents = f"{type(status_code)}<br>{status_code}"
        send_email(subject="Tweet Collection - Error", contents=contents)

    def on_limit(self, track):
        print("RATE LIMITING", type(track))
        print(track)
        contents = f"{type(track)}<br>{track}"
        send_email(subject="Tweet Collection - Rate Limit", contents=contents)

    def on_timeout(self):
        print("TIMEOUT!")
        send_email(subject="Tweet Collection - Timeout", contents="Restarting...")
        return True # don't kill the stream! TODO: implement back-off

    def on_warning(self, notice):
        print("DISCONNECTION WARNING:", type(notice))
        print(notice)
        contents = f"{type(notice)}<br>{notice}"
        send_email(subject="Tweet Collection - Disconnect Warning", contents=contents)

    def on_disconnect(self, notice):
        print("DISCONNECT:", type(notice))
        contents = f"{type(notice)}<br>{notice}"
        send_email(subject="Tweet Collection - Disconnect", contents=contents)

if __name__ == "__main__":

    print("COLLECTING TWEETS IN", APP_ENV.upper())

    listener = TweetCollector()
    print("LISTENER", type(listener))

    stream = Stream(listener.auth, listener)
    print("STREAM", type(stream))

    print("TOPICS:", TOPICS_LIST)
    stream.filter(track=TOPICS_LIST)

    # this never gets reached
