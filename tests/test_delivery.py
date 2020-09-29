import pytest
from delivery import SlackDelivery
from prettyconf import config

SLACK_API_TOKEN = config('SLACK_API_TOKEN')
SLACK_CHANNEL = config('SLACK_CHANNEL')


@pytest.fixture
def delivery_service():
    yield SlackDelivery(SLACK_API_TOKEN, SLACK_CHANNEL)


def test_setup(delivery_service):
    assert delivery_service is not None
