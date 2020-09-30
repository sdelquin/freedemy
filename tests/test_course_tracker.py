import os

import pytest
from course_tracker import CT_Twitter
import settings

API_WINDOW_SIZE = 10
LAST_MANAGED_TWEET_FILE = 'last-managed-tweet.test'
SEARCH_TERMS_FILE = 'search-terms.test'


@pytest.fixture
def course_tracker():
    yield CT_Twitter(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_SECRET_KEY,
        twitter_target_account=settings.TWITTER_TARGET_ACCOUNT,
        last_managed_tweet_file=LAST_MANAGED_TWEET_FILE,
        api_window_size=API_WINDOW_SIZE,
        search_terms_file=SEARCH_TERMS_FILE,
    )
    os.remove(LAST_MANAGED_TWEET_FILE)
    os.remove(SEARCH_TERMS_FILE)


def test_get_matching_tweets(course_tracker):
    assert len(list(course_tracker.get_matching_tweets())) == API_WINDOW_SIZE
