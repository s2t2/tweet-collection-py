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
        self.max = 25 # TODO: set via env var

    def on_connect(self):
        print("LISTENER IS CONNECTED!")

    def on_status(self, status):
        self.counter +=1
        if self.counter > self.max:
            print("COLLECTION COMPLETE!")
            print("SHUTTING DOWN...")

        print("----------------")
        print(f"DETECTED AN INCOMING TWEET! ({self.counter})")
        print(status.user.screen_name, "says:", status.text)
        # todo: store the tweet! (to CSV in dev, to BQ in production)
        breakpoint()
        #pprint(status)

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
