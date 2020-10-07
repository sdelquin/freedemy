from logzero import logfile, logger

import settings
from promo import Course, get_valid_course_locales

logfile(
    settings.LOGFILE,
    maxBytes=settings.LOGFILE_SIZE,
    backupCount=settings.LOGFILE_BACKUP_COUNT,
)


def manage_course(course_tracker_url, delivery_service):
    logger.debug(f'Managing {course_tracker_url}')

    valid_course_locales = get_valid_course_locales(settings.VALID_COURSE_LOCALES_FILE)

    course = Course(
        course_tracker_url,
        settings.UDEMY_COURSES_BASE_URL,
        valid_course_locales,
    )

    logger.debug('Coupons:')
    for coupon in course.coupons:
        logger.debug(
            f'{coupon["code"]} | valid: {coupon["isValid"]} | {coupon["discountValue"]}'
        )

    if course.is_valid():
        delivery_service.post(course)
    else:
        logger.warning('Current course is not valid. Skipping...')
