import json
import os

import requests
from bs4 import BeautifulSoup
from prettyconf import config


class Course:
    def __init__(self, course_tracker_url):
        self.course_tracker_url = course_tracker_url
        self.courses_base_url = config('UDEMY_COURSES_BASE_URL')
        self.get_course_tracker_data()

    def get_course_tracker_data(self):
        response = requests.get(self.course_tracker_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find(id='__NEXT_DATA__')
        self.next_data = json.loads(element.string)

    @property
    def coupon(self):
        return self.next_data['props']['pageProps']['course']['coupon'][0]['code']

    @property
    def slug(self):
        return self.next_data['query']['cleanUrl']

    @property
    def title(self):
        return self.next_data['props']['pageProps']['course']['detail'][0]['title']

    @property
    def url(self):
        return os.path.join(self.courses_base_url, self.slug, f'?couponCode={self.coupon}')

    def __str__(self):
        return f'{self.title}\n{self.url}'
