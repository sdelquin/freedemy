import json
import os
from pathlib import Path
from string import Template

import requests
from bs4 import BeautifulSoup
from logzero import logger


class Course:
    ''' Represent a course in Udemy '''

    def __init__(self, course_tracker_url, courses_base_url):
        logger.info('Building Udemy course...')
        self.course_tracker_url = course_tracker_url
        self.courses_base_url = courses_base_url
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
    def url(self):
        return os.path.join(self.courses_base_url, self.slug, f'?couponCode={self.coupon}')

    def is_valid(self):
        return all((self.url is not None, self.slug is not None, self.title is not None))

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
