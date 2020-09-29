from prettyconf import config

from course_tracker import CT_Twitter
from delivery import SlackDelivery
from promo import Course

CONSUMER_KEY = config('TWITTER_API_KEY')
CONSUMER_SECRET = config('TWITTER_SECRET_KEY')
TWITTER_TARGET_ACCOUNT = config('TWITTER_TARGET_ACCOUNT')
LAST_MANAGED_TWEET_FILE = config('LAST_MANAGED_TWEET_FILE')
API_WINDOW_SIZE = config('API_WINDOW_SIZE', cast=int)
SEARCH_TERMS_FILE = config('SEARCH_TERMS_FILE')
SLACK_API_TOKEN = config('SLACK_API_TOKEN')
SLACK_CHANNEL = config('SLACK_CHANNEL')

t = CT_Twitter(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    TWITTER_TARGET_ACCOUNT,
    LAST_MANAGED_TWEET_FILE,
    API_WINDOW_SIZE,
    SEARCH_TERMS_FILE,
)

d = SlackDelivery(SLACK_API_TOKEN, SLACK_CHANNEL)

for url in t.get_couponed_course_tracker_urls():
    c = Course(url)
    d.post(c)
t.update_last_managed_tweet_file()
