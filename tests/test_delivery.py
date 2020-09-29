import pytest
from delivery import SlackDelivery
from prettyconf import config
from promo import Course

COURSE_TRACKER_TEST_URL = config('COURSE_TRACKER_TEST_URL')
SLACK_API_TOKEN = config('SLACK_API_TOKEN')
SLACK_CHANNEL = config('SLACK_CHANNEL')


@pytest.fixture
def delivery_service():
    return SlackDelivery(SLACK_API_TOKEN, SLACK_CHANNEL)


@pytest.fixture
def course():
    c = Course(COURSE_TRACKER_TEST_URL)
    c.get_course_tracker_data()
    return c


def test_post(delivery_service, course):
    assert delivery_service.post(course) is not None
