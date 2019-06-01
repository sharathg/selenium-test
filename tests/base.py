import unittest
import logging
import json

from os.path import join
from os.path import dirname
from os import environ
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from time import sleep


class BaseTest(unittest.TestCase):

    # ===============
    # Class Variables
    # ===============
    driver = None
    logger = None
    testSuiteStartTime = None
    config = {}
    handler = None
    file_handler = None

    # ================
    # TestCase Methods
    # ================
    @classmethod
    def setUpClass(cls):
        cls.init_logger()
        cls.testSuiteStartTime = cls.timestamp()
        cls.driver = cls.init_driver()

    def setUp(self):
        self.logger.info("*** Running Test: {} ***".format(self._testMethodName))
        self.testStartTime = self.timestamp()

    def tearDown(self):
        if self._failure:
            self.logger.error("Test Failed ! ERROR: {}".format(self._failure))
        self.testTime = self.timestamp() - self.testStartTime
        self.logger.info("*** Finished Test: {} (Time: {}) ***\n\n".format(self._testMethodName, self.testTime))

    @classmethod
    def tearDownClass(cls):
        cls.testSuiteTime = cls.timestamp() - cls.testSuiteStartTime
        cls.logger.info("*** Finished Suite. Time: {} ***".format(cls.testSuiteTime))
        cls.quit_logger()
        cls.quit_driver()

    def run(self, result=None):
        self._failure = False
        try:
            super().run(result)
        except Exception as e:
            self._failure = e
            raise e

    # ============
    # Time Methods
    # ============
    @classmethod
    def timestamp(cls, microseconds=False):
        return datetime.now() if microseconds else datetime.now().replace(microsecond=0)

    @classmethod
    def quick_wait(cls, seconds=0.1):
        sleep(seconds)

    # ==============
    # Logger Methods
    # ==============
    @classmethod
    def init_logger(cls):
        if not cls.logger:
            cls.logger = logging.getLogger("selenium-test")
            cls.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(funcName)s(%(lineno)d)] :: %(message)s')
            formatter.default_time_format = '%H:%M:%S'
            cls.handler = logging.StreamHandler()
            cls.handler.setLevel(logging.DEBUG)
            cls.handler.setFormatter(formatter)
            cls.logger.addHandler(cls.handler)
            cls.file_handler = logging.FileHandler("script.log")
            cls.file_handler.setLevel(logging.DEBUG)
            cls.file_handler.setFormatter(formatter)
            cls.logger.addHandler(cls.file_handler)

    @classmethod
    def quit_logger(cls):
        try:
            cls.logger.info("Closing Logger.")
            cls.logger.removeHandler(cls.handler)
            cls.logger.removeHandler(cls.file_handler)
        except Exception as e:
            print("*** Error Removing Logger Handler. Error: {} ***\n\n\n".format(e))
        cls.logger = None

    # ==============
    # Driver Methods
    # ==============
    @classmethod
    def init_driver(cls):
        cls.config = cls.config_data("{}.config".format(environ.get("BROWSER", "chrome")), '../configs')
        options = ChromeOptions() if cls.config['browserName'].lower() == 'chrome' else FirefoxOptions()
        for opt in cls.config['browserOptions']:
            options.add_argument(opt)
        if cls.config['browserName'].lower() == 'chrome':
            return Chrome(chrome_options=options)
        else:
            return Firefox(firefox_options=options)

    @classmethod
    def quit_driver(cls):
        cls.driver.quit()

    @classmethod
    def clear_cookies(cls):
        cls.driver.delete_all_cookies()

    @classmethod
    def current_url(cls):
        return cls.driver.current_url

    @classmethod
    def title(cls):
        return cls.driver.title

    # ===========
    # Config Data
    # ===========
    @classmethod
    def config_data(cls, filename, directory=""):
        relative_path = join(directory, filename)
        absolute_path = join(dirname(__file__), relative_path)
        with open(absolute_path) as config_file:
            return json.loads(config_file.read())

    # ==============
    # Assert Methods
    # ==============
    def assertEqual(self, first, second, msg=None):
        try:
            super().assertEqual(first, second, msg)
            self.logger.info("Assert [{}] :: {} == {} ? Result :: True".format(msg, first, second))
        except AssertionError as ae:
            self.logger.error("Assertion ERROR !!\n[{}]\nActual: {}\nExpected: {}".format(msg, first, second))
            raise ae

    def assertNotEqual(self, first, second, msg=None):
        try:
            super().assertNotEqual(first, second, msg)
            self.logger.info("Assert [{}] :: {} != {} ? Result :: True".format(msg, first, second))
        except AssertionError as ae:
            self.logger.error("Assertion ERROR !!\n[{}]\nActual: {}\nNOT Expected: {}".format(msg, first, second))
            raise ae

    def assertIn(self, member, container, msg=None):
        try:
            super().assertIn(member, container, msg)
            self.logger.info("Assert [{}] :: {} IN {} ? Result :: True".format(msg, member, container))
        except AssertionError as ae:
            self.logger.error("Assertion ERROR !!\n[{}]\nMember: {}\nContainer: {}".format(msg, container, member))
            raise ae

    def assertTrue(self, expr, msg=None):
        try:
            super().assertTrue(expr, msg)
            self.logger.info("Assert [{}] :: {} == TRUE ? Result :: True".format(msg, expr))
        except AssertionError as ae:
            self.logger.error("Assertion ERROR !!\n[{}]\nExpression Value: {}\nExpected: TRUE".format(msg, expr))
            raise ae

    def assertFalse(self, expr, msg=None):
        try:
            super().assertFalse(expr, msg)
            self.logger.info("Assert [{}] :: {} == FALSE ? Result :: True".format(msg, expr))
        except AssertionError as ae:
            self.logger.error("Assertion ERROR !!\n[{}]\nExpression Value: {}\nExpected: FALSE".format(msg, expr))
            raise ae

    def assertIsNotNone(self, obj, msg=None):
        try:
            super().assertTrue(obj, msg)
            self.logger.info("Assert [{}] :: {} != NONE ? Result :: True".format(msg, obj))
        except AssertionError as ae:
            self.logger.error("Assertion ERROR !!\n[{}]\nObject: {}\nExpected: Not NONE".format(msg, obj))
            raise ae