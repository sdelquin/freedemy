from pathlib import Path

import pytest
from prettyconf import config

from freedemy.promo import Course

COURSE_PROPERTIES = (
    'slug',
    'coupon',
    'title',
    'price',
    'rating',
    'subscribers',
    'discount_price',
    'locale',
    'url',
    'language',
    'language_flag',
    'coupons',
)


@pytest.fixture
def course(request):
    marker = request.node.get_closest_marker('course_tracker_url')
    course_tracker_url = marker.args[0] if marker is not None else marker
    marker = request.node.get_closest_marker('valid_course_locales')
    valid_course_locales = marker.args[0] if marker is not None else []

    c = Course(course_tracker_url, valid_course_locales)
    c.get_course_tracker_data()
    return c


@pytest.mark.course_tracker_url(config('COURSE_TRACKER_TEST_URL'))
def test_get_course_tracker_data(course):
    assert isinstance(course.course_info, dict)


@pytest.mark.course_tracker_url(config('COURSE_TRACKER_TEST_URL'))
def test_course_properties(course):
    for property in COURSE_PROPERTIES:
        assert getattr(course, property) != ''


@pytest.mark.course_tracker_url(config('COURSE_TRACKER_TEST_URL'))
def test_str(course):
    course_rep_length = len(Path('course.tmpl').read_text().split('\n'))
    assert len(str(course).split('\n')) == course_rep_length


@pytest.mark.course_tracker_url(config('COURSE_TRACKER_TEST_URL'))
@pytest.mark.valid_course_locales(['en_US'])
def test_valid_locale(course):
    assert course.has_valid_locale() is True


@pytest.mark.course_tracker_url(config('COURSE_TRACKER_ARABIC_TEST_URL'))
@pytest.mark.valid_course_locales(['es_ES'])
def test_invalid_locale(course):
    assert course.has_valid_locale() is False


@pytest.mark.course_tracker_url(config('COURSE_TRACKER_TEST_URL'))
@pytest.mark.valid_course_locales([])
def test_empty_locales(course):
    assert course.has_valid_locale() is True


@pytest.mark.course_tracker_url(config('COURSE_TRACKER_TEST_URL'))
@pytest.mark.valid_course_locales([])
def test_course_language(course):
    assert course.language_flag == '🇺🇸'
