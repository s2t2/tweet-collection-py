
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
