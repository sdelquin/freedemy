from logzero import logger
from slack import WebClient
from slack.errors import SlackApiError

import settings
from promo import Course


class SlackDelivery:
    def __init__(
        self, slack_api_token=settings.SLACK_API_TOKEN, slack_channel=settings.SLACK_CHANNEL
    ):
        logger.info('Building Slack service for delivery...')
        self.client = WebClient(slack_api_token)
        self.slack_channel = slack_channel

    def post(self, course: Course):
        logger.info('Posting course info in Slack channel...')
        try:
            return self.client.chat_postMessage(
                channel=self.slack_channel, text=str(course)
            )
        except SlackApiError as e:
            logger.error(e.response['error'])
