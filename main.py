from prettyconf import config
from course_tracker import CT_Twitter
from promo import Course

CONSUMER_KEY = config('TWITTER_API_KEY')
CONSUMER_SECRET = config('TWITTER_SECRET_KEY')
TWITTER_TARGET_ACCOUNT = config('TWITTER_TARGET_ACCOUNT')
LAST_MANAGED_TWEET_FILE = config('LAST_MANAGED_TWEET_FILE')
API_WINDOW_SIZE = config('API_WINDOW_SIZE', cast=int)
MATCHING_RULES_FILE = config('MATCHING_RULES_FILE')

t = CT_Twitter(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    TWITTER_TARGET_ACCOUNT,
    LAST_MANAGED_TWEET_FILE,
    API_WINDOW_SIZE,
    MATCHING_RULES_FILE,
)

for url in t.get_couponed_course_tracker_urls():
    c = Course(url)
    print(c, end='\n')
t.update_last_managed_tweet_file()
