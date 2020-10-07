from datetime import timedelta

from redis import Redis
from rq import Queue

import settings
import tasks
from course_tracker import CT_Twitter
from delivery import SlackDelivery
from utils import init_logger

logger = init_logger()


def run():
    course_queue = Queue(settings.REDIS_QUEUE, connection=Redis())
    course_tracker = CT_Twitter(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_SECRET_KEY,
        course_tracker_twitter=settings.COURSE_TRACKER_TWITTER,
        last_managed_tweet_file=settings.LAST_MANAGED_TWEET_FILE,
        api_window_size=settings.TWITTER_API_WINDOW_SIZE,
        search_terms_file=settings.SEARCH_TERMS_FILE,
    )
    delivery_service = SlackDelivery(settings.SLACK_API_TOKEN, settings.SLACK_CHANNEL)
    for url in course_tracker.get_couponed_course_tracker_urls():
        logger.info(
            f'Enqueuing {url} for processing in {settings.JOB_EXECUTION_TIMEDELTA}s ...'
        )
        course_queue.enqueue_in(
            timedelta(seconds=settings.JOB_EXECUTION_TIMEDELTA),
            tasks.manage_course,
            url,
            delivery_service,
        )
    course_tracker.update_last_managed_tweet_file()


if __name__ == '__main__':
    run()
