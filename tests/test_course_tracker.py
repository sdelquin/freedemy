import os

import pytest
import settings
from course_tracker import CT_Twitter
from promo import Course

API_WINDOW_SIZE = 10
LAST_MANAGED_TWEET_FILE = 'last-managed-tweet.test'
SEARCH_TERMS_FILE = 'search-terms.test'


@pytest.fixture
def course_tracker():
    yield CT_Twitter(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_SECRET_KEY,
        course_tracker_twitter=settings.COURSE_TRACKER_TWITTER,
        last_managed_tweet_file=LAST_MANAGED_TWEET_FILE,
        api_window_size=API_WINDOW_SIZE,
        search_terms_file=SEARCH_TERMS_FILE,
    )
    os.remove(LAST_MANAGED_TWEET_FILE)
    os.remove(SEARCH_TERMS_FILE)


def test_get_matching_tweets(course_tracker):
    assert len(list(course_tracker.get_matching_tweets())) == API_WINDOW_SIZE


def test_course_expiration_message(course_tracker):
    last_url = list(course_tracker.get_couponed_course_tracker_urls())[-1]
    last_course = Course(last_url)
    assert last_course.get_expiration_message() is not None
