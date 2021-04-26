import re
from pathlib import Path
from string import Template

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

    def __init__(self, course_tracker_url, valid_course_locales=[]):
        logger.info('Building Udemy course...')

        options = Options()
        options.headless = True
        self.webdriver = webdriver.Firefox(options=options)

        self.course_tracker_url = course_tracker_url
        self.valid_course_locales = valid_course_locales
        self.get_contents()
        if self.url:
            self.extract_features()

    def get_contents(self) -> str:
        '''Returns html for main div of course'''
        self.webdriver.get(self.course_tracker_url)
        element = WebDriverWait(self.webdriver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="__next"]/div/div[1]/div/div/div/div[4]/button/span[1]')
            )
        )
        if '100%OFF' in element.text:
            element.click()
            try:
                self.webdriver.switch_to.window(self.webdriver.window_handles[1])
                element = WebDriverWait(self.webdriver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'main-content-wrapper'))
                )
                self.contents = element.get_attribute('innerHTML')
                self.url = self.webdriver.current_url
            except TimeoutException:
                logger.error('Timeout waiting for page loading')
                self.contents = ''
                self.url = ''
            finally:
                self.webdriver.quit()

    def extract_features(self):
        soup = BeautifulSoup(self.contents, 'html.parser')
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

        # element = soup.find('div', {'data-purpose': 'course-old-price-text'})
        # print(element)
        # element = element.find_all('span')[1].s.span
        # self.old_price = float(re.search(r'[\d.]+', element.string.strip()).group())

        # element = soup.find('div', {'data-purpose': 'discount-percentage'})
        # element = element.find_all('span')[1].span
        # self.discount_percentage = float(
        #     re.search(r'[\d.]+', element.string.strip()).group()
        # )
        # self.discount_price = self.old_price - (
        #     (100 - self.discount_percentage) * self.old_price
        # )

        element = soup.find('div', {'data-purpose': 'lead-course-locale'})
        self.locale = element.get_text().strip()

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
