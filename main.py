import settings
from course_tracker import CT_Twitter
from delivery import SlackDelivery
from promo import Course
from utils import init_logger

logger = init_logger()


def run():
    course_tracker = CT_Twitter(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_SECRET_KEY,
        course_tracker_twitter=settings.COURSE_TRACKER_TWITTER,
        last_managed_tweet_file=settings.LAST_MANAGED_TWEET_FILE,
        api_window_size=settings.TWITTER_API_WINDOW_SIZE,
        search_terms_file=settings.SEARCH_TERMS_FILE,
    )

    delivery_service = SlackDelivery(settings.SLACK_API_TOKEN, settings.SLACK_CHANNEL)

    for ct_url in course_tracker.get_course_tracker_urls():
        if (
            course := Course(
                ct_url, settings.UDEMY_API_BASE_URL, settings.PROXY_FOR_UDEMY_REQUESTS
            )
        ).is_valid:
            delivery_service.post(course)
        else:
            logger.info('Discarding course: not valid...')
    course_tracker.update_last_managed_tweet_file()


if __name__ == '__main__':
    run()
