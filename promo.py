import json
import os

import requests
from bs4 import BeautifulSoup
from prettyconf import config


class Course:
    ''' Represent a course in Udemy '''

    def __init__(self, course_tracker_url):
        self.course_tracker_url = course_tracker_url
        self.courses_base_url = config('UDEMY_COURSES_BASE_URL')
        self.get_course_tracker_data()

    def get_course_tracker_data(self):
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
        return f'{self.title}\n{self.url}'

    def get_course_info(self):
        return '\n'.join(
            map(
                str,
                [
                    self.headline,
                    self.price,
                    self.rating,
                    self.subscribers,
                    self.discount_price,
                ],
            )
        )
