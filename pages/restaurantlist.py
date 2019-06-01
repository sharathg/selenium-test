from pages.base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class RestaurantListPage(BasePage):

    # ===================
    # Inherited Constants
    # ===================
    driver = None
    logger = None

    # =========
    # Test Data
    # =========
    TEST_RESTAURANTS_LIST_URL = "https://www.thuisbezorgd.nl/eten-bestellen-enschede-8889"
    TEST_ZIPCODE = "8889"
    TEST_ADDRESS = "{}, 8889AA".format(TEST_ZIPCODE)
    TEST_RESTAURANT_NAME = "QA Restaurant Selenium"
    TEST_RESTAURANT_URL = "https://www.thuisbezorgd.nl/qa-restaurant-selenium"

    # ========
    # Locators
    # ========
    DROP_DOWN_LOCATION = (By.ID, "dropdown-location")
    KITCHEN_TYPES_CONTAINER = (By.ID, "kitchen-types")
    FILTER_SIDEBAR = (By.CLASS_NAME, "restaurants-filter")
    RESTAURANTS_LIST_CONTAINER = (By.ID, "irestaurantlist")
    RESTAURANT_ELEM = (By.CLASS_NAME, "restaurant")
    LOGO_WRAPPER = (By.CLASS_NAME, "logowrapper")
    DETAILS_WRAPPER = (By.CLASS_NAME, "detailswrapper")
    RESTAURANT_NAME = (By.TAG_NAME, "a")

    # ============
    # Page Methods
    # ============
    def open_restaurants_list_page(self):
        self.logger.info("Opening URL: {}".format(self.TEST_RESTAURANTS_LIST_URL))
        self.driver.get(self.TEST_RESTAURANTS_LIST_URL)

    def is_restaurants_list_page(self):
        return self.get_elements(self.DROP_DOWN_LOCATION) != []

    def get_location_drop_down(self):
        return self.get_element(self.DROP_DOWN_LOCATION)

    def get_kitchen_types_container(self):
        return self.get_element(self.KITCHEN_TYPES_CONTAINER)

    def get_filter_sidebar(self):
        return self.get_element(self.FILTER_SIDEBAR)

    def get_restaurant_list_container(self):
        return self.get_element(self.RESTAURANTS_LIST_CONTAINER)

    def get_restaurants_list(self):
        return self.get_elements(self.RESTAURANT_ELEM, self.get_restaurant_list_container())

    def get_logo_wrapper(self, restaurant_elem):
        return self.get_element(self.LOGO_WRAPPER, restaurant_elem)

    def get_details_wrapper(self, restaurant_elem):
        return self.get_element(self.DETAILS_WRAPPER, restaurant_elem)

    def get_restaurant_name(self, restaurant_details_wrapper):
        return self.get_element(self.RESTAURANT_NAME, restaurant_details_wrapper).text

    def get_qa_restaurant(self):
        res_list = self.get_restaurants_list()
        for res in res_list:
            if self.get_restaurant_name(self.get_details_wrapper(res)) == self.TEST_RESTAURANT_NAME:
                return res
        return None
