import pytest
import settings
from delivery import SlackDelivery
from promo import Course


@pytest.fixture
def delivery_service():
    return SlackDelivery(settings.SLACK_API_TOKEN, settings.SLACK_CHANNEL)


@pytest.fixture
def course():
    c = Course(settings.COURSE_TRACKER_TEST_URL, settings.UDEMY_COURSES_BASE_URL)
    c.get_course_tracker_data()
    return c


def test_post(delivery_service, course):
    assert delivery_service.post(course) is not None
