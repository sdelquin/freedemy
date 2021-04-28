import re
from pathlib import Path
from string import Template
from urllib import parse as urlparse

import requests
from bs4 import BeautifulSoup
from logzero import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings


class Course:
    ''' Represent a course in Udemy '''

    def __init__(
        self,
        course_tracker_url,
        api_base_url=settings.UDEMY_API_BASE_URL,
        proxy_for_udemy_requests=settings.PROXY_FOR_UDEMY_REQUESTS,
        geckodriver_logfile=settings.GECKODRIVER_LOGFILE,
    ):
        logger.info('Building Udemy course...')

        options = Options()
        options.headless = True
        self.webdriver = webdriver.Firefox(options=options, log_path=geckodriver_logfile)

        self.course_tracker_url = course_tracker_url
        self.api_base_url = api_base_url
        self.proxy_for_udemy_requests = proxy_for_udemy_requests

        try:
            self.get_contents()
        except Exception as err:
            logger.error(err)
        else:
            if self.is_couponed:
                self.extract_web_features()
                self.extract_api_features()
        finally:
            self.webdriver.quit()

    def get_contents(self) -> str:
        logger.info('Getting html contents...')

        self.webdriver.get(self.course_tracker_url)
        element = WebDriverWait(self.webdriver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="__next"]/div/div[1]/div/div/div/div[4]/button/span[1]')
            )
        )
        if '100%OFF' in element.text:
            self.is_couponed = True
            element.click()
            self.webdriver.switch_to.window(self.webdriver.window_handles[1])
            element = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ud-app-loaded'))
            )
            self.contents = element.get_attribute('outerHTML')
            self.url = self.webdriver.current_url
        else:
            self.is_couponed = False

    def extract_web_features(self):
        logger.info('Extracting course web features...')

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
        self._locale = element.get_text().strip().upper()

    def extract_api_features(self):
        logger.info('Extracting course api features...')

        if self.proxy_for_udemy_requests:
            logger.warning(f'Using {self.proxy_for_udemy_requests} as proxy...')
            proxies = {
                'http': self.proxy_for_udemy_requests,
                'https': self.proxy_for_udemy_requests,
            }
            response = requests.get(self.api_url, proxies=proxies)
        else:
            response = requests.get(self.api_url)

        fields = response.json()

        aux = fields['price_text']['data']['pricing_result']['price']['amount']
        self.new_price = int(aux) if int(aux) == aux else aux
        aux = fields['price_text']['data']['pricing_result']['list_price']['amount']
        self.old_price = int(aux) if int(aux) == aux else aux
        aux = fields['discount_expiration']['data']['discount_deadline_text']
        quant, units = re.search(r'^(\d+)\s+(.)', aux).groups()
        mfactor = 24 if units == 'd' else 1
        self.expiration = int(quant) * mfactor

    @property
    def has_valid_locale(self):
        return self.locale in ('🇺🇸', '🇪🇸')

    @property
    def locale(self):
        if self._locale in ('ENGLISH', 'INGLÉS'):
            return '🇺🇸'
        elif self._locale in ('SPANISH', 'ESPAÑOL'):
            return '🇪🇸'
        else:
            return '🏳'

    @property
    def is_valid(self):
        try:
            return all([self.url, self.contents, self.is_couponed, self.has_valid_locale])
        except AttributeError:
            return False

    def __str__(self):
        template = Template(Path('course.tmpl').read_text())
        return template.substitute(
            title=self.title,
            headline=self.headline,
            rating=self.rating,
            enrollments=self.enrollments,
            locale=self.locale,
            expiration=self.expiration,
            old_price=self.old_price,
            new_price=self.new_price,
            url=self.url,
        )
