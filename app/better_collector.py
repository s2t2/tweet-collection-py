import os
from dotenv import load_dotenv

from tweepy import Stream
from urllib3.exceptions import ProtocolError

from app.tweet_collector import TweetCollector as MyListener
from app.storage_service import local_topics

load_dotenv()

TWITTER_HANDLE = os.getenv("TWITTER_HANDLE")

class BetterCollector():
    def __init__(self):
        self.listener = MyListener()
        print("LISTENER", type(listener))
        self.stream = Stream(listener.auth, listener)
        print("STREAM", type(stream))
        #self.topics = stream.listener.topics
        self.__set_topics__()

    def __set_topics__(self):
        if STORAGE_ENV == "remote":
            rows = self.listener.bq_service.fetch_topics()
            self.topics = [row.topic for row in rows]
        else:
            self.topics = local_topics()

        if TWITTER_HANDLE and TWITTER_HANDLE not in self.topics:
            self.topics.append(TWITTER_HANDLE.strip()) # track the app's handle, so we can respond to mentions

        print("SET TOPICS:", self.topics)

    def collect(self):
        print("COLLECTING!")
        # h/t: https://stackoverflow.com/questions/23601634/how-to-restart-tweepy-script-in-case-of-error
        try:
            print("[STREAM] Started steam")
            self.stream.filter(track=self.topics)
        except Exception as ex:
            print("[STREAM] Stream stopped! Reconnecting to twitter stream")
            print ex.message, ex.args
            self.collect()

if __name__ == "__main__":

    collector = BetterCollector()
    collector.collect()

    print("THIS NEVER GETS REACHED")
