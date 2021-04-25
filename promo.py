from pathlib import Path
from string import Template

from logzero import logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Course:
    ''' Represent a course in Udemy '''

    def __init__(self, course_tracker_url, valid_course_locales=[]):
        logger.info('Building Udemy course...')

        options = Options()
        options.headless = False
        self.webdriver = webdriver.Firefox(options=options)

        self.course_tracker_url = course_tracker_url
        self.valid_course_locales = valid_course_locales
        self.contents = self.get_contents()

    def get_contents(self) -> WebElement:
        '''Returns main div of course'''
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
                return element
            except TimeoutException:
                logger.error('Timeout waiting for page loading')
            finally:
                self.webdriver.quit()

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
            language_flag=self.language_flag,
        )
