import json
import os
from pathlib import Path
from string import Template

import requests
from bs4 import BeautifulSoup
from logzero import logger
from prettyconf import config


class Course:
    ''' Represent a course in Udemy '''

    def __init__(self, course_tracker_url):
        logger.info('Building Udemy course...')
        self.course_tracker_url = course_tracker_url
        self.courses_base_url = config('UDEMY_COURSES_BASE_URL')
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
        return self.next_data['query']['cleanUrl']

    @property
    def coupon(self):
        return self.course_info['coupon'][0]['code']

    @property
    def title(self):
        return self.course_info['detail'][0]['title']

    @property
    def headline(self):
        return self.course_info['detail'][0]['headline']

    @property
    def price(self):
        return self.course_info['detail'][0]['price'] / 100

    @property
    def rating(self):
        return self.course_info['detail'][0]['rating']

    @property
    def subscribers(self):
        return self.course_info['detail'][0]['subscribers']

    @property
    def discount_price(self):
        return self.course_info['coupon'][0]['discountPrice']

    @property
    def url(self):
        return os.path.join(self.courses_base_url, self.slug, f'?couponCode={self.coupon}')

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
