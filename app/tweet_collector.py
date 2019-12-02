import os
from pprint import pprint

from dotenv import load_dotenv
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from app import APP_ENV

load_dotenv()

CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY", default="OOPS")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET", default="OOPS")
ACCESS_KEY = os.getenv("TWITTER_ACCESS_TOKEN", default="OOPS")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", default="OOPS")

TOPICS_LIST = ["impeach"] # todo: dynamically compile list from comma-separated env var string like "topic1,topic2"

class TweetCollector(StreamListener):

    def __init__(self):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(self.auth)
        self.counter = 0
        self.max = 25 # TODO: config via env var

    def parse_status(self, status):
        twt = status._json
        usr = twt["user"]

        if twt["truncated"] and twt["extended_tweet"]:
            full_text = twt["extended_tweet"]["full_text"]
        else:
            full_text = twt["text"]

        tweet = {
            "id_str": twt["id_str"],
            #"in_reply_to_status_id_str": twt["in_reply_to_status_id_str"],
            "created_at": twt["created_at"], #> 'Mon Dec 02 01:06:52 +0000 2019'
            #"timestamp_ms": twt["timestamp_ms"],
            "geo": twt["geo"], #> None or __________
            "full_text": full_text, #> 'Refuse censure! Make them try to impeach and beat it. Mr President you are guilty of no crime. Continue the exposure of these subversives that are so desperate to smear you for draining the swamp!'
        }

        user = {
            "id_str": usr["id_str"],
            "description": usr["description"],
            "screen_name": usr["screen_name"],
            "utc_offset": usr["utc_offset"],
            "location": usr["location"],
            "verified": usr["verified"],
            #"geo_enabled": usr["geo_enabled"],
        }

        return tweet, user

    def is_collectable(self, status):
        if status.lang == "en" and status.user.verified:
            return True
        else:
            return False

    def on_status(self, status):
        if self.is_collectable(status):
            self.counter +=1
            #if self.counter > self.max:
            #    print("COLLECTION COMPLETE!")
            #    print("SHUTTING DOWN...")
            #    # TODO: exit() or return False or something
            print("----------------")
            print(f"DETECTED AN INCOMING TWEET! ({self.counter})")
            #print(status.user.screen_name, "says:", status.text)
            tweet, user = self.parse_status(status)
            print("TWEET", tweet)
            print("USER", user)
            # todo: store tweet and user (to CSV in dev, to BQ in production)

    def on_connect(self):
        print("LISTENER IS CONNECTED!")

    def on_exception(self, exception):
        print("EXCEPTION:", type(exception))
        print(exception)

    def on_error(self, status_code):
        print("ERROR:", status_code)

    def on_limit(self, track):
        print("RATE LIMITING", type(track))
        print(track)

    def on_timeout(self):
        print("TIMEOUT!")
        #print("STAYING ALIVE...")
        #return True # don't kill the stream! TODO: implement back-off

    def on_warning(self, notice):
        print("DISCONNECTION WARNING:", type(notice))
        print(notice)

    def on_disconnect(self, notice):
        print("DISCONNECT:", type(notice))
        print(notice)

if __name__ == "__main__":

    print("COLLECTING TWEETS IN", APP_ENV.upper())

    listener = TweetCollector()
    print("LISTENER", type(listener))

    stream = Stream(listener.auth, listener)
    print("STREAM", type(stream))

    print("TOPICS:", TOPICS_LIST)
    stream.filter(track=TOPICS_LIST) #TODO: track=listener.topics_list

    # this never gets reached
