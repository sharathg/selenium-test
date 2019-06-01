from pages.base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class HomePage(BasePage):

    # ===================
    # Inherited Constants
    # ===================
    driver = None
    logger = None

    # =========
    # Test Data
    # =========
    TITLE = "Thuisbezorgd"
    DEFAULT_LOCALE = 'NL'
    HOME_PAGE_URL = "https://www.thuisbezorgd.nl"
    TEST_RESTAURANTS_LIST_URL = "https://www.thuisbezorgd.nl/eten-bestellen-enschede-8889"
    TEST_ADDRESS = "8889AA"

    # ========
    # Locators
    # ========
    LOCALE_BUTTON = (By.ID, "locale")
    LOCALE_CONTAINER = (By.CLASS_NAME, "language-country-modal")
    LOCALE_FLAGS = {
        'nl': (By.CLASS_NAME, "locale-flag-nl"),
        'en': (By.CLASS_NAME, "locale-flag-en"),
        'de': (By.CLASS_NAME, "locale-flag-de")
    }
    HEADLINES = (By.CLASS_NAME, "headlines")
    DELIVERY_AREA_FORM = (By.ID, "ideliveryareaform")
    ADDRESS_TEXT_BOX = (By.ID, "imysearchstring")
    SUBMIT_BUTTON = (By.ID, "submit_deliveryarea")
    AUTOCOMPLETE_DROP_DOWN_CONTENT = (By.ID, "iautoCompleteDropDownContent")

    # ============
    # Page Methods
    # ============
    def open_home_page(self):
        self.logger.info("Opening URL: {}".format(self.HOME_PAGE_URL))
        self.driver.get(self.HOME_PAGE_URL)

    def is_home_page(self):
        return self.get_elements(self.ADDRESS_TEXT_BOX) != []

    def get_current_locale(self):
        locale = self.get_element(self.LOCALE_BUTTON).get_attribute('class')[-2:]
        self.logger.info("Current Locale: {}".format(locale))
        return locale

    def get_delivery_area_form(self):
        return self.get_element(self.DELIVERY_AREA_FORM)

    def get_address_text_box(self, delivery_area_form=None):
        if not delivery_area_form:
            delivery_area_form = self.get_delivery_area_form()
        return self.get_element(self.ADDRESS_TEXT_BOX, delivery_area_form)

    def get_autocomplete_drop_down(self, delivery_area_form=None):
        if not delivery_area_form:
            delivery_area_form = self.get_delivery_area_form()
        return self.get_element(self.AUTOCOMPLETE_DROP_DOWN_CONTENT, delivery_area_form)

    def get_submit_button(self, delivery_area_form=None):
        if not delivery_area_form:
            delivery_area_form = self.get_delivery_area_form()
        return self.get_element(self.SUBMIT_BUTTON, delivery_area_form)

    def click_outside_address_box(self):
        self.get_element(self.HEADLINES).click()

    def press_enter_in_address_box(self):
        self.get_address_text_box().send_keys(Keys.ENTER)

    def type_in_address_box(self, text):
        address_box = self.get_address_text_box()
        self.logger.info("Present Address Box Value: {}".format(address_box.get_attribute("value")))
        address_box.click()
        address_box.send_keys(text)
        self.logger.info("Updated Address Box Value: {}".format(address_box.get_attribute("value")))

    def clear_address_box(self):
        address_box = self.get_address_text_box()
        self.logger.info("Present Address Box Value: {}".format(address_box.get_attribute("value")))
        address_box.clear()
        self.logger.info("Updated Address Box Value: {}".format(address_box.get_attribute("value")))

    def get_address_box_value(self):
        address_box = self.get_address_text_box()
        self.logger.info("Present Address Box Value: {}".format(address_box.get_attribute("value")))
        return address_box.get_attribute("value")

    def wait_for_drop_down(self, timeout=3):
        self.wait_for_clickable(self.AUTOCOMPLETE_DROP_DOWN_CONTENT, self.get_delivery_area_form(), timeout)

    def change_locale(self, locale='en'):
        if self.get_current_locale().lower() == locale.lower():
            self.logger.info("Present Locale already: {}. No need to change".format(locale.upper()))
        else:
            self.logger.info("Present Locale: {}".format(self.get_current_locale().upper()))
            self.get_element(self.LOCALE_BUTTON).click()
            locale_container = self.get_element(self.LOCALE_CONTAINER)
            self.get_element(self.LOCALE_FLAGS[locale], locale_container).click()
            self.logger.info("Locale Changed to {}.".format(self.get_current_locale().upper()))

    def set_test_address(self):
        self.logger.info("Set Test Address: ({}) to Address Text Box.".format(self.TEST_ADDRESS))
        self.get_element(self.ADDRESS_TEXT_BOX).send_keys(self.TEST_ADDRESS)

    def search_using_test_address(self):
        self.set_test_address()
        self.logger.info("Press Enter on the Address Text Box.")
        self.get_element(self.ADDRESS_TEXT_BOX).send_keys(Keys.ENTER)
