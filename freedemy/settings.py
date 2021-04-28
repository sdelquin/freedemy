from prettyconf import config

TWITTER_API_KEY = config('TWITTER_API_KEY')
TWITTER_SECRET_KEY = config('TWITTER_SECRET_KEY')
SLACK_API_TOKEN = config('SLACK_API_TOKEN')
SLACK_CHANNEL = config('SLACK_CHANNEL')
COURSE_TRACKER_TWITTER = config('COURSE_TRACKER_TWITTER', default='comidoc')
COURSE_TRACKER_BASE_URL = config('COURSE_TRACKER_BASE_URL', default='https://comidoc.net')
LAST_MANAGED_TWEET_FILE = config(
    'LAST_MANAGED_TWEET_FILE', default='last-managed-tweet.dat'
)
SEARCH_TERMS_FILE = config('SEARCH_TERMS_FILE', default='search-terms.dat')
TWITTER_API_WINDOW_SIZE = config('TWITTER_API_WINDOW_SIZE', cast=int, default=10)
UDEMY_API_BASE_URL = config(
    'UDEMY_API_BASE_URL',
    default='https://www.udemy.com/api-2.0/course-landing-components/{course_id}'
    '/me/?couponCode={coupon_code}&components=price_text,discount_expiration',
)
LOGFILE = config('LOGFILE', default='freedemy.log')
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)
PROXY_FOR_UDEMY_REQUESTS = config('PROXY_FOR_UDEMY_REQUESTS', default='')
