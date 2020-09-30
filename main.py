from logzero import logfile, logger

import settings
from course_tracker import CT_Twitter
from delivery import SlackDelivery
from promo import Course

# Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
logfile(settings.LOGFILE, maxBytes=1e6, backupCount=3)

t = CT_Twitter(
    settings.TWITTER_API_KEY,
    settings.TWITTER_SECRET_KEY,
    settings.TWITTER_TARGET_ACCOUNT,
    settings.LAST_MANAGED_TWEET_FILE,
    settings.API_WINDOW_SIZE,
    settings.SEARCH_TERMS_FILE,
)

d = SlackDelivery(settings.SLACK_API_TOKEN, settings.SLACK_CHANNEL)

for url in t.get_couponed_course_tracker_urls():
    logger.debug(f'Managing {url}')
    c = Course(url, settings.UDEMY_COURSES_BASE_URL)
    if c.is_valid():
        d.post(c)
    else:
        logger.warning('Current course is not valid. Skipping...')
t.update_last_managed_tweet_file()
