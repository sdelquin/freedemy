import re
from pathlib import Path
from string import Template
from urllib import parse as urlparse

from bs4 import BeautifulSoup
from logzero import logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Course:
    ''' Represent a course in Udemy '''

    def __init__(self, course_tracker_url, api_base_url):
        logger.info('Building Udemy course...')

        options = Options()
        options.headless = True
        self.webdriver = webdriver.Firefox(options=options)

        self.course_tracker_url = course_tracker_url
        self.api_base_url = api_base_url
        if self.get_contents():
            self.extract_features()

    def get_contents(self) -> str:
        logger.info('Getting html contents...')

        self.webdriver.get(self.course_tracker_url)
        element = WebDriverWait(self.webdriver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="__next"]/div/div[1]/div/div/div/div[4]/button/span[1]')
            )
        )
        self.contents, self.url = '', ''
        if '100%OFF' in element.text:
            self.is_couponed = True
            element.click()
            try:
                self.webdriver.switch_to.window(self.webdriver.window_handles[1])
                element = WebDriverWait(self.webdriver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ud-app-loaded'))
                )
                self.contents = element.get_attribute('outerHTML')
                self.url = self.webdriver.current_url
            except TimeoutException:
                logger.error('Timeout waiting for page loading')
            finally:
                # TODO: Move to the constructor to quit webdriver in anycase
                self.webdriver.quit()
        else:
            self.is_couponed = False
        return self.contents

    def extract_features(self):
        logger.info('Extracting course features...')

        soup = BeautifulSoup(self.contents, 'html.parser')

        element = soup.find('body')
        self.course_id = element['data-clp-course-id'].strip()

        element = urlparse.parse_qs(urlparse.urlparse(self.url).query)
        self.coupon_code = element['couponCode'][0]

        self.api_url = self.api_base_url.format(
            course_id=self.course_id, coupon_code=self.coupon_code
        )

        element = soup.find('h1', {'data-purpose': 'lead-title'})
        self.title = element.string.strip()

        element = soup.find('div', {'data-purpose': 'lead-headline'})
        self.headline = element.string.strip()

        element = soup.find('span', {'data-purpose': 'rating-number'})
        self.rating = float(element.string.strip().replace(',', '.'))

        element = soup.find('div', {'data-purpose': 'enrollment'})
        self.enrollments = int(
            re.search(r'[\d,.]+', element.string.strip())
            .group()
            .replace('.', '')
            .replace(',', '')
        )

        element = soup.find('div', {'data-purpose': 'lead-course-locale'})
        self.locale = element.get_text().strip()

    @property
    def has_valid_locale(self):
        return hasattr(self, 'locale') and self.locale.lower() in (
            'english',
            'spanish',
            'inglés',
            'español',
        )

    @property
    def is_valid(self):
        return all([self.url, self.contents, self.is_couponed, self.has_valid_locale])

    def __str__(self):
        template = Template(Path('course.tmpl').read_text())
        return template.substitute(
            title=self.title,
            headline=self.headline,
            rating=self.rating,
            enrollments=self.enrollments,
            locale=self.locale,
            url=self.url,
        )
