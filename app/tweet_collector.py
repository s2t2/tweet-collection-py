import os
from pprint import pprint
from time import sleep

from dotenv import load_dotenv
from tweepy.streaming import StreamListener
from tweepy import Stream
from urllib3.exceptions import ProtocolError

from app import APP_ENV, STORAGE_ENV
from app.twitter_service import twitter_api
from app.notification_service import send_email
from app.storage_service import append_to_csv, BigQueryService

load_dotenv()

#TOPICS_LIST = ["impeach", "impeachment"] # todo: dynamically compile list from comma-separated env var string like "topic1,topic2"
# NOTE: "impeachment" keywords don't trigger the "impeach" filter, so adding "impeachment" as well
#TOPICS_LIST = ["impeach -filter:retweets"] # doesn't work
TOPICS = os.getenv("TOPICS", default="impeach, impeached, impeachment, #TrumpImpeachment, #ImpeachAndConvict, #ImpeachAndConvictTrump, #IGReport, #SenateHearing, #IGHearing")

BATCH_SIZE = int(os.getenv("BATCH_SIZE", default="20")) # coerces to int
WILL_NOTIFY = (os.getenv("WILL_NOTIFY", default="False") == "True") # coerces to bool

def topics_list(topics_csv_str=TOPICS):
    return [topic.strip() for topic in topics_csv_str.split(",")]

def is_collectable(status):
    """Param status (tweepy.models.Status)"""
    return (status.lang == "en"
            #and status.user.verified
            #and status.in_reply_to_status_id == None
            #and status.in_reply_to_user_id == None
            #and status.in_reply_to_screen_name == None
            #and status.is_quote_status == False
            #and status.retweeted == False
            #and not hasattr(status, "retweeted_status")
    )

def backoff_strategy(i):
    """
    Param: i (int) increasing rate limit number from the twitter api
    Returns: number of seconds to sleep for
    """
    return (int(i) + 1) ** 2 # raise to the power of two

class TweetCollector(StreamListener):

    def __init__(self, batch_size=BATCH_SIZE, will_notify=WILL_NOTIFY):
        self.api = twitter_api()
        self.auth = self.api.auth
        self.counter = 0
        self.bq_service = BigQueryService()
        self.batch_size = batch_size
        self.batch = []
        self.will_notify = (will_notify == True)

    def collect_in_batches(self, status):
        """
        Param status (tweepy.models.Status)
        Moving this logic out of on_status in hopes of preventing ProtocolErrors
        Storing in batches to reduce API calls, and in hopes of preventing ProtocolErrors
        """
        parsed_status = parse_status(status)
        if APP_ENV != "production":
            pprint(parsed_status)

        self.batch.append(parsed_status)

        if len(self.batch) >= self.batch_size:
            print("STORING BATCH OF", len(self.batch), "TWEETS...")

            if STORAGE_ENV == "local":
                append_to_csv(self.batch)
            elif STORAGE_ENV == "remote":
                self.bq_service.append_to_bq(self.batch)

            print("CLEARING BATCH AND COUNTER...")
            self.batch = []
            self.counter = 0

    def on_status(self, status):
        """Param status (tweepy.models.Status)"""
        if is_collectable(status):
            self.counter +=1
            ###if self.counter > 3: raise RuntimeError("OOPS")
            print("----------------")
            print(f"DETECTED AN INCOMING TWEET! ({self.counter} -- {status.id_str})")
            self.collect_in_batches(status)

    def on_connect(self):
        print("LISTENER IS CONNECTED!")
        print("LISTENER WILL NOTIFY:", self.will_notify)

    def on_exception(self, exception):
        # has encountered errors:
        #  + urllib3.exceptions.ProtocolError: ('Connection broken: IncompleteRead(0 bytes read)'
        #  + urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool
        print("EXCEPTION:", type(exception))
        print(exception)
        if self.will_notify:
            contents = f"{type(exception)}<br>{exception}"
            send_email(subject="Tweet Collection - Exception", contents=contents)

    def on_error(self, status_code):
        print("ERROR:", status_code)
        if self.will_notify:
            contents = f"{type(status_code)}<br>{status_code}"
            send_email(subject="Tweet Collection - Error", contents=contents)

    def on_limit(self, track):
        """Param: track (int) starts low and subsequently increases"""
        print("RATE LIMITING", track)
        if self.will_notify:
            contents = f"{type(track)}<br>{track}"
            send_email(subject="Tweet Collection - Rate Limit", contents=contents)
        sleep_seconds = backoff_strategy(track)
        print("SLEEPING FOR:", sleep_seconds, "SECONDS...")
        sleep(sleep_seconds)

    def on_timeout(self):
        print("TIMEOUT!")
        if self.will_notify:
            send_email(subject="Tweet Collection - Timeout", contents="Restarting...")
        return True # don't kill the stream! TODO: implement back-off

    def on_warning(self, notice):
        print("DISCONNECTION WARNING:", type(notice))
        print(notice)
        if self.will_notify:
            contents = f"{type(notice)}<br>{notice}"
            send_email(subject="Tweet Collection - Disconnect Warning", contents=contents)

    def on_disconnect(self, notice):
        print("DISCONNECT:", type(notice))
        if self.will_notify:
            contents = f"{type(notice)}<br>{notice}"
            send_email(subject="Tweet Collection - Disconnect", contents=contents)

if __name__ == "__main__":

    print("COLLECTING TWEETS TO", STORAGE_ENV.upper(), "STORAGE")

    listener = TweetCollector()
    print("LISTENER", type(listener))

    stream = Stream(listener.auth, listener)
    print("STREAM", type(stream))

    topics = topics_list()
    print("TOPICS:", topics)
    #stream.filter(track=topics)
    # handle ProtocolErrors...
    while True:
        try:
            stream.filter(track=topics)
        except ProtocolError:
            print("--------------------------------")
            print("RESTARTING AFTER PROTOCOL ERROR!")
            continue

    # this never gets reached
