import pytest

import settings
from freedemy.delivery import SlackDelivery
from freedemy.promo import Course

# Spanish Free Course
FREE_COURSE_URL = 'https://comidoc.net/udemy/fundamentos-de-big-data-en-aws'
# English Couponed Course
COUPONED_COURSE_URL = (
    'https://comidoc.net/udemy/nginx-apache-ssl-encryption-certification-course'
)


@pytest.fixture
def delivery_service():
    return SlackDelivery(settings.SLACK_API_TOKEN, settings.SLACK_CHANNEL)


@pytest.fixture
def free_course():
    return Course(FREE_COURSE_URL)


@pytest.fixture
def couponed_course():
    return Course(COUPONED_COURSE_URL)
