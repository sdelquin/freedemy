import json
import os
from pathlib import Path
from string import Template

import requests
from bs4 import BeautifulSoup
from logzero import logger


def get_valid_course_locales(valid_course_locales_file):
    logger.info('Getting valid course locales from file...')
    f = Path(valid_course_locales_file)
    if f.exists():
        # split('.') helps when locales like es_ES.UTF-8 are found
        valid_course_locales = [c.split('.')[0] for c in f.read_text().strip().split('\n')]
    else:
        logger.warning('File of valid course locales not found. All locales are valid.')
        valid_course_locales = []
    return valid_course_locales


class Course:
    ''' Represent a course in Udemy '''

    def __init__(self, course_tracker_url, courses_base_url, valid_course_locales=[]):
        logger.info('Building Udemy course...')
        self.course_tracker_url = course_tracker_url
        self.courses_base_url = courses_base_url
        self.valid_course_locales = valid_course_locales
        self.get_course_tracker_data()

    def get_course_tracker_data(self):
        logger.info('Getting Udemy course information...')
        response = requests.get(self.course_tracker_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find(id='__NEXT_DATA__')
        self.next_data = json.loads(element.string)
        # to improve readability (in further accesses)
        self.course_info = self.next_data['props']['pageProps']['course']

    @property
    def slug(self):
        try:
            return self.next_data['query']['cleanUrl']
        except Exception:
            logger.error('Unable to locate slug')

    @property
    def coupon(self):
        try:
            return self.course_info['coupon'][0]['code']
        except Exception:
            logger.error('Unable to locate coupon')

    @property
    def title(self):
        try:
            return self.course_info['detail'][0]['title']
        except Exception:
            logger.error('Unable to locate title')

    @property
    def headline(self):
        try:
            return self.course_info['detail'][0]['headline']
        except Exception:
            logger.error('Unable to locate headline')

    @property
    def price(self):
        try:
            return self.course_info['detail'][0]['price'] / 100
        except Exception:
            logger.error('Unable to locate price')

    @property
    def rating(self):
        try:
            return self.course_info['detail'][0]['rating']
        except Exception:
            logger.error('Unable to locate rating')

    @property
    def subscribers(self):
        try:
            return self.course_info['detail'][0]['subscribers']
        except Exception:
            logger.error('Unable to locate subscribers')

    @property
    def discount_price(self):
        try:
            return self.course_info['coupon'][0]['discountPrice']
        except Exception:
            logger.error('Unable to locate discount price')

    @property
    def locale(self):
        try:
            return self.course_info['detail'][0]['locale']['locale'].strip()
        except Exception:
            logger.error('Unable to locate locale')

    @property
    def url(self):
        return os.path.join(self.courses_base_url, self.slug, f'?couponCode={self.coupon}')

    def has_valid_locale(self):
        logger.info('Checking if course has valid locale...')
        if self.locale is not None:
            if self.valid_course_locales:
                if not (valid := self.locale in self.valid_course_locales):
                    logger.error(f'"{self.locale}" is not a valid locale')
                return valid
            else:
                # no locales specified => all are valids!
                return True
        return False

    def is_valid(self):
        logger.info('Checking if course is valid...')
        return all(
            (
                self.coupon is not None,
                self.slug is not None,
                self.title is not None,
                self.has_valid_locale(),
            )
        )

    @property
    def coupons(self):
        return self.next_data['props']['pageProps']['coupons']

    def __str__(self):
        template = Template(Path('course.tmpl').read_text())
        return template.substitute(
            title=self.title,
            headline=self.headline,
            rating=round(self.rating, 2),
            subscribers=self.subscribers,
            price=self.price,
            discount_price=self.discount_price,
            url=self.url,
        )

    def as_dict(self):
        return dict(
            title=self.title,
            url=self.url,
            headline=self.headline,
            price=self.price,
            discount_price=self.discount_price,
            rating=self.rating,
            subscribers=self.subscribers,
        )
