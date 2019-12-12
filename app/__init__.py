import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", default="impeachment") # OR choose your own project name
APP_ENV = os.getenv("APP_ENV", default="development") # "development" OR "production"
STORAGE_ENV = os.getenv("STORAGE_ENV", default="local") # "local" OR "remote"

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
