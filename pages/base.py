from os.path import join
from os.path import dirname
from datetime import datetime
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp_cond
from selenium.common.exceptions import TimeoutException


class BasePage:

    # ===============
    # Class Variables
    # ===============
    driver = None
    logger = None
    testSuiteStartTime = None
    config = {}
    handler = None
    file_handler = None

    # ============
    # Time Methods
    # ============
    @classmethod
    def timestamp(cls, microseconds=False):
        return datetime.now() if microseconds else datetime.now().replace(microsecond=0)

    @classmethod
    def quick_wait(cls, seconds=0.1):
        sleep(seconds)

    # ============
    # File Methods
    # ============
    @classmethod
    def file_data(cls, filename, directory=""):
        relative_path = join(directory, filename)
        absolute_path = join(dirname(__file__), relative_path)
        with open(absolute_path) as file:
            return file.read()

    # ===================
    # Get Element Methods
    # ===================
    def get_elements(self, locator, base_elem=None, timeout=None):
        s = self.timestamp()
        self.driver.implicitly_wait(0)
        temp_elem_list = []
        tries = timer = 0
        if not base_elem:
            base_elem = self.driver
            base_elem_name = "WebDriver"
        else:
            base_elem_name = base_elem.tag_name
        if not timeout:
            timeout = self.config['implicitWaitTime']
        while not temp_elem_list:
            if timer >= timeout:
                break
            temp_elem_list = base_elem.find_elements(*locator)
            self.quick_wait()
            timer = (self.timestamp() - s).seconds
            tries += 1
        if not temp_elem_list:
            self.logger.warning(
                "*** TEST CASE PROBABLE FAIL *** Element Not Found ! [Tries: {}, Time: {}] "
                "BaseElement: {}, LocatorStategy: {}, LocatorString: {}".format(
                    tries, timeout, base_elem_name, *locator))
        else:
            self.logger.info(
                "Element Found ! [Tries: {}, Time: {}] BaseElement: {}, LocatorStrategy: {}, LocatorString: {}".format(
                    tries, timer, base_elem_name, *locator))
        return temp_elem_list

    def get_element(self, locator, base_elem=None, timeout=None):
        temp_elem_list = self.get_elements(locator, base_elem, timeout)
        try:
            return temp_elem_list[0]
        except IndexError as ie:
            self.logger.error(ie)
            raise Exception("Element Not Found: {}, {}".format(*locator))

    # ===============
    # Wait For Methods
    # ===============
    def __wait_for__(self, wait_type, locator=None, base_elem=None, timeout=5):
        if not base_elem:
            base_elem = self.driver
            base_elem_name = "WebDriver"
        else:
            base_elem_name = base_elem.tag_name
        wait = WebDriverWait(base_elem, timeout)
        try:
            wait.until(wait_type(locator))
        except TimeoutException as TE:
            TE.msg = "Element did not appear. BaseElement: {}, LocatorStrategy: {}, LocatorString: {}".format(
                base_elem_name, *locator)
            raise TE

    def wait_for_presence(self, locator, base_elem=None, timeout=5):
        self.__wait_for__(exp_cond.presence_of_element_located, locator, base_elem, timeout)

    def wait_for_clickable(self, locator, base_elem=None, timeout=5):
        self.__wait_for__(exp_cond.element_to_be_clickable, locator, base_elem, timeout)

    def wait_for_document_ready(self, timeout=5):
        start = self.timestamp()
        timer = (self.timestamp() - start).seconds
        status = self.driver.execute_script("return document.readyState")
        while timer <= timeout and status.lower() != "complete":
            sleep(0.1)
            status = self.driver.execute_script("return document.readyState")
            timer = (self.timestamp() - start).seconds

    def wait_for_new_page_load(self, timeout=10):
        start = self.timestamp()
        page_url = self.driver.current_url
        timer = (self.timestamp() - start).seconds
        while timer <= timeout and self.driver.current_url in [page_url, "loading"]:
            sleep(0.1)
            timer = (self.timestamp() - start).seconds
        status = self.driver.execute_script("return document.readyState")
        while timer <= timeout and status.lower() != "complete":
            sleep(0.1)
            status = self.driver.execute_script("return document.readyState")
            timer = (self.timestamp() - start).seconds
