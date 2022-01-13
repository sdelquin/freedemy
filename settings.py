from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path('.').resolve()

TWITTER_API_KEY = config('TWITTER_API_KEY')
TWITTER_SECRET_KEY = config('TWITTER_SECRET_KEY')
TWITTER_API_WINDOW_SIZE = config('TWITTER_API_WINDOW_SIZE', cast=int, default=10)

SLACK_API_TOKEN = config('SLACK_API_TOKEN')
SLACK_CHANNEL = config('SLACK_CHANNEL')

COURSE_TRACKER_TWITTER = config('COURSE_TRACKER_TWITTER', default='comidoc')
COURSE_TRACKER_BASE_URL = config('COURSE_TRACKER_BASE_URL', default='https://comidoc.net')

LAST_MANAGED_TWEET_FILE = config(
    'LAST_MANAGED_TWEET_FILE', default=PROJECT_DIR / 'data' / 'last-managed-tweet.txt'
)
SEARCH_TERMS_FILE = config(
    'SEARCH_TERMS_FILE', default=PROJECT_DIR / 'data' / 'search-terms.txt'
)
COURSE_TEMPLATE_FILE = config(
    'COURSE_TEMPLATE_FILE', default=PROJECT_DIR / 'data' / 'course.tmpl'
)

UDEMY_API_BASE_URL = config(
    'UDEMY_API_BASE_URL',
    default='https://www.udemy.com/api-2.0/course-landing-components/{course_id}'
    '/me/?couponCode={coupon_code}&components=price_text,discount_expiration',
)

LOGFILE = config('LOGFILE', default=PROJECT_DIR / 'data' / 'freedemy.log')
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)
GECKODRIVER_LOGFILE = config(
    'GECKODRIVER_LOGFILE', default=PROJECT_DIR / 'data' / 'geckodriver.log'
)

PROXY_FOR_UDEMY_REQUESTS = config('PROXY_FOR_UDEMY_REQUESTS', default='')

COUPON_BUTTON_XPATH = config(
    'COUPON_BUTTON_XPATH',
    default='//*[@id="__next"]/div/div/article/div[4]/div/div[2]/div/button',
)
