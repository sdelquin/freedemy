from prettyconf import config

TWITTER_API_KEY = config('TWITTER_API_KEY')
TWITTER_SECRET_KEY = config('TWITTER_SECRET_KEY')
SLACK_API_TOKEN = config('SLACK_API_TOKEN')
SLACK_CHANNEL = config('SLACK_CHANNEL')
TWITTER_TARGET_ACCOUNT = config('TWITTER_TARGET_ACCOUNT', default='comidoc')
COURSE_TRACKER_BASE_URL = config('COURSE_TRACKER_BASE_URL', default='https://comidoc.net')
LAST_MANAGED_TWEET_FILE = config(
    'LAST_MANAGED_TWEET_FILE', default='last-managed-tweet.dat'
)
SEARCH_TERMS_FILE = config('SEARCH_TERMS_FILE', default='search-terms.dat')
API_WINDOW_SIZE = config('API_WINDOW_SIZE', cast=int, default=10)
UDEMY_COURSES_BASE_URL = config(
    'UDEMY_COURSES_BASE_URL', default='https://www.udemy.com/course/'
)
LOGFILE = config('LOGFILE', default='freedemy.log')
