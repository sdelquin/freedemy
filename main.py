from course_tracker import CT_Twitter
from delivery import SlackDelivery
from promo import Course
from utils import init_logger

logger = init_logger()


def run():
    course_tracker = CT_Twitter()
    delivery_service = SlackDelivery()

    for ct_url in course_tracker.get_course_tracker_urls():
        if (course := Course(ct_url)).is_valid:
            delivery_service.post(course)
        else:
            logger.info('Discarding course: not valid...')

    course_tracker.update_last_managed_tweet_file()


if __name__ == '__main__':
    run()
