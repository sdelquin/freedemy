from logzero import logfile, logger

import settings
from course_tracker import CT_Twitter
from delivery import SlackDelivery
from promo import Course

# Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
logfile(settings.LOGFILE, maxBytes=1e6, backupCount=3)

course_tracker = CT_Twitter(
    settings.TWITTER_API_KEY,
    settings.TWITTER_SECRET_KEY,
    settings.TWITTER_TARGET_ACCOUNT,
    settings.LAST_MANAGED_TWEET_FILE,
    settings.API_WINDOW_SIZE,
    settings.SEARCH_TERMS_FILE,
)

delivery = SlackDelivery(settings.SLACK_API_TOKEN, settings.SLACK_CHANNEL)

for url in course_tracker.get_couponed_course_tracker_urls():
    logger.debug(f'Managing {url}')
    course = Course(url, settings.UDEMY_COURSES_BASE_URL)
    if course.is_valid():
        delivery.post(course)
    else:
        logger.warning('Current course is not valid. Skipping...')

course_tracker.update_last_managed_tweet_file()
