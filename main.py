from logzero import logfile, logger
from prettyconf import config

from course_tracker import CT_Twitter
from delivery import SlackDelivery
from promo import Course

CONSUMER_KEY = config('TWITTER_API_KEY')
CONSUMER_SECRET = config('TWITTER_SECRET_KEY')
TWITTER_TARGET_ACCOUNT = config('TWITTER_TARGET_ACCOUNT')
LAST_MANAGED_TWEET_FILE = config(
    'LAST_MANAGED_TWEET_FILE', default='last-managed-tweet.dat'
)
API_WINDOW_SIZE = config('API_WINDOW_SIZE', cast=int, default=10)
SEARCH_TERMS_FILE = config('SEARCH_TERMS_FILE', default='search-terms.dat')
SLACK_API_TOKEN = config('SLACK_API_TOKEN')
SLACK_CHANNEL = config('SLACK_CHANNEL')
LOGFILE = config('LOGFILE', default='freedemy.log')

# Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
logfile(LOGFILE, maxBytes=1e6, backupCount=3)

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
    logger.debug(f'Managing {url}')
    c = Course(url)
    d.post(c)
t.update_last_managed_tweet_file()
