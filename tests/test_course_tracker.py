import os

import pytest

from freedemy import settings
from freedemy.course_tracker import CT_Twitter

TWITTER_API_WINDOW_SIZE = 10
LAST_MANAGED_TWEET_FILE = 'last-managed-tweet.test'
SEARCH_TERMS_FILE = 'search-terms.test'


@pytest.fixture
def course_tracker(request):
    marker = request.node.get_closest_marker('twitter_api_window_size')
    api_window_size = marker.args[0] if marker is not None else TWITTER_API_WINDOW_SIZE

    yield CT_Twitter(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_SECRET_KEY,
        course_tracker_twitter=settings.COURSE_TRACKER_TWITTER,
        last_managed_tweet_file=LAST_MANAGED_TWEET_FILE,
        api_window_size=api_window_size,
        search_terms_file=SEARCH_TERMS_FILE,
    )
    os.remove(LAST_MANAGED_TWEET_FILE)
    os.remove(SEARCH_TERMS_FILE)


def test_get_course_tracker_urls(course_tracker):
    urls = list(course_tracker.get_course_tracker_urls())
    assert len(urls) == TWITTER_API_WINDOW_SIZE
    assert all(urls)
