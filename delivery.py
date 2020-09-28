from slack import WebClient
from slack.errors import SlackApiError
from promo import Course


class SlackDelivery:
    def __init__(self, slack_api_token, slack_channel):
        self.client = WebClient(slack_api_token)
        self.slack_channel = slack_channel

    def post(self, course: Course):
        try:
            self.client.chat_postMessage(channel=self.slack_channel, text=str(course))
        except SlackApiError as e:
            # You will get a SlackApiError if 'ok' is False
            assert e.response['ok'] is False
            assert e.response['error']  # str like 'invalid_auth', 'channel_not_found'
            print(f'Got an error: {e.response["error"]}')
