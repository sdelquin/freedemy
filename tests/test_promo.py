from pathlib import Path

import pytest
import settings
from prettyconf import config
from promo import Course

COURSE_PROPERTIES = (
    'slug',
    'coupon',
    'title',
    'price',
    'rating',
    'subscribers',
    'discount_price',
    'url',
)


@pytest.fixture
def course():
    c = Course(config('COURSE_TRACKER_TEST_URL'), settings.UDEMY_COURSES_BASE_URL)
    c.get_course_tracker_data()
    return c


def test_get_course_tracker_data(course):
    assert isinstance(course.course_info, dict)


def test_course_properties(course):
    for property in COURSE_PROPERTIES:
        assert getattr(course, property) != ''


def test_str(course):
    course_rep_length = len(Path('course.tmpl').read_text().split('\n'))
    assert len(str(course).split('\n')) == course_rep_length
