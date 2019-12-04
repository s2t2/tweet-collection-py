
import pytest

from app.twitter_service import twitter_api as api

@pytest.fixture(scope="module")
def twitter_api():
    return api()

@pytest.fixture(scope="module")
def my_status(twitter_api):
    return twitter_api.get_status(1201357629928411136)

@pytest.fixture(scope="module")
def rr_status(twitter_api):
    return twitter_api.get_status(1201308452850675712, tweet_mode="extended")

@pytest.fixture()
def mock_tweet():
    return {
        'id_str': '12345',
        'full_text': 'My mock tweet text',
        'geo': None,
        'created_at': '2019-12-02 01:13:49',
        'user_id_str': '98776655443',
        'user_screen_name': 'user123',
        'user_description': 'Testing the storage service',
        'user_location': '',
        'user_verified': False
    }
