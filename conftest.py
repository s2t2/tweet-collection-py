import os
import pytest

from app.twitter_service import twitter_api as api
from app.storage_service import BigQueryService
from app.tweet_collector import TweetCollector

DATA_DIR = os.path.join(os.path.dirname(__file__), "test", "data")
MOCK_TOPICS_CSV_FILEPATH = os.path.join(DATA_DIR, "mock_topics.csv")

#
# BIGQUERY API CALLS
#

@pytest.fixture(scope="module")
def bq_service():
    return BigQueryService(dataset_name="impeachment_test")

@pytest.fixture(scope="module")
def listener(bq_service):
    return TweetCollector(
        bq_service=bq_service, # todo: convert to storage service
        dev_handle="@dev_account",
        admin_handles=["@admin1", "@admin2"],
        topics_csv_filepath=MOCK_TOPICS_CSV_FILEPATH # todo: move to storage service
    )

@pytest.fixture(scope="module")
def handleless_listener(bq_service):
    return TweetCollector(bq_service=bq_service, dev_handle=None, admin_handles=None, topics_csv_filepath=MOCK_TOPICS_CSV_FILEPATH)

#
# TWITTER API CALLS
#

@pytest.fixture(scope="module")
def twitter_api():
    return api()

@pytest.fixture(scope="module")
def tweet(twitter_api):
    """mimics the data returned by the listener's on_status() method"""
    return twitter_api.get_status(1201308452850675712)

@pytest.fixture(scope="module")
def tweet_ext(twitter_api):
    """extended mode gets more data than the listener's on_status method"""
    return twitter_api.get_status(1201308452850675712, tweet_mode="extended")

@pytest.fixture(scope="module")
def retweet(twitter_api):
    """mimics the data returned by the listener's on_status() method"""
    return twitter_api.get_status(1201341021432365056)

@pytest.fixture(scope="module")
def retweet_ext(twitter_api):
    """extended mode gets more data than the listener's on_status method"""
    return twitter_api.get_status(1201341021432365056, tweet_mode="extended")

#@pytest.fixture(scope="module")
#def tweet_with_weird_user_description_1(twitter_api):
#    return twitter_api.get_status(1205017687216336896)
#
#@pytest.fixture(scope="module")
#def tweet_with_weird_user_description_2(twitter_api):
#    return twitter_api.get_status(1205017997162606594)

@pytest.fixture(scope="module")
def admin_add_topic_tweet(twitter_api):
    #return twitter_api.get_status(1205337492695728133) # doesn't have colon
    return twitter_api.get_status(1207089823988760576)

#
# MOCKS
#

tweet_attributes = {
    'status_id': '1201308452850675712',
    'status_text': 'There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are… https://t.co/uHrShOKq8f',
    'truncated': True,
    'retweet_status_id': None,
    'reply_status_id': None,
    'reply_user_id': None,
    'is_quote': False,
    'geo': None,
    'created_at': '2019-12-02 01:13:49',
    'user_id': '148529707',
    'user_name': 'Robert Reich',
    'user_screen_name': 'RBReich',
    'user_description': 'Berkeley prof, former Sec. of Lab. @InequalityMedia. Movies "Saving Capitalism" & "Inequality for All" on Netflix. Books: The Common Good, Saving Capitalism,etc',
    'user_location': 'Berkeley, CA',
    'user_verified': True,
    'user_created_at': '2010-05-26 23:17:10'
}

retweet_attributes = {
    'status_id': '1201341021432365056',
    'status_text': 'RT @RBReich: There’s zero chance that 20 Republican senators have enough integrity to remove Trump from office.   But there are still 3 rea…',
    'truncated': False,
    'retweet_status_id': "1201308452850675712", # status.id
    'reply_status_id': None,
    'reply_user_id': None,
    'is_quote': False,
    'geo': None,
    'created_at': '2019-12-02 03:23:14',
    'user_id': '1188953381152231425',
    'user_name': 'Donald Olson',
    'user_screen_name': 'DonaldO36048407',
    'user_description': 'You tell me what you think , I will tell you what I think . If we agree fine , If not fine , lets keep talking !',
    'user_location': '',
    'user_verified': False,
    'user_created_at': '2019-10-28 23:00:46'
}

@pytest.fixture()
def parsed_tweet():
    return tweet_attributes

@pytest.fixture()
def parsed_retweet():
    return retweet_attributes
