
import pytest

from app.tweet_collector import TweetCollector

# prevents unnecessary or duplicative api requests
# fixture only loaded when a specific test needs it
# module-level fixture only invoked once for all tests
@pytest.fixture(scope="module")
def my_status():
    listener = TweetCollector()
    return listener.api.get_status(1201357629928411136)

@pytest.fixture(scope="module")
def rr_status():
    listener = TweetCollector()
    return listener.api.get_status(1201308452850675712, tweet_mode="extended")
