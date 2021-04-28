COURSE_FEATURES = (
    'title',
    'headline',
    'rating',
    'enrollments',
    'locale',
    'expiration',
    'old_price',
    'new_price',
    'url',
    'api_url',
    'course_id',
    'coupon_code',
)


def test_valid_course(couponed_course):
    assert couponed_course.is_valid


def test_invalid_course(free_course):
    assert not free_course.is_valid


def test_course_features(couponed_course):
    assert all(
        [str(getattr(couponed_course, feature)) != '' for feature in COURSE_FEATURES]
    )


def test_locale(couponed_course):
    assert couponed_course.locale == '🇺🇸'
