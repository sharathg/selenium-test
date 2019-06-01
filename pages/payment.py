from pages.base import BasePage
from selenium.webdriver.common.by import By


class PaymentPage(BasePage):

    # ===================
    # Inherited Constants
    # ===================
    driver = None
    logger = None

    # =========
    # Test Data
    # =========
    QA_RESTAURANT_PAYMENT_URL = "https://www.thuisbezorgd.nl/bestelling-afronden-qa-restaurant-selenium"
    TEST_ADDRESS = "8889AA"
    CASH_PAYMENT = {
        'nl': "Contant",
        'en': "Cash payment"
    }

    # ========
    # Locators
    # ========
    CHECKOUT_FORM = (By.ID, "checkoutform")
    ADDRESS_BOX = (By.ID, "iaddress")
    POSTCODE_BOX = (By.ID, "ipostcode")
    CITY_BOX = (By.ID, "itown")
    NAME_BOX = (By.ID, "isurname")
    EMAIL_BOX = (By.ID, "iemail")
    PHONE_BOX = (By.ID, "iphonenumber")
    COMPANY_BOX = (By.ID, "icompanyname")
    DELIVERY_TIME = (By.ID, "ideliverytime")
    REMARKS_AREA = (By.ID, "iremarks")
    PAYMENT_BUTTONS = (By.CLASS_NAME, "paymentbuttonwrapper")
    PAYMENT_ORDER_BUTTON = (By.CLASS_NAME, "checkout-orderbutton-btn")
    BANK_SELECT_FOR_IDEAL = (By.ID, "iidealbank")
    BANK_OPTION = (By.TAG_NAME, "option")
    FAILED_PAYMENT_RETRY_BUTTON = (By.CLASS_NAME, "button-retry")

    # ============
    # Page Methods
    # ============
    def open_payment_page(self):
        self.logger.info("Opening URL: {}".format(self.QA_RESTAURANT_PAYMENT_URL))
        self.driver.get(self.QA_RESTAURANT_PAYMENT_URL)

    def is_payment_page(self):
        return self.get_elements(self.CHECKOUT_FORM) != []

    def get_checkout_form(self):
        return self.get_element(self.CHECKOUT_FORM)

    def get_address_box(self):
        return self.get_element(self.ADDRESS_BOX, self.get_checkout_form())

    def get_postcode_box(self):
        return self.get_element(self.POSTCODE_BOX, self.get_checkout_form())

    def get_city_box(self):
        return self.get_element(self.CITY_BOX, self.get_checkout_form())

    def get_name_box(self):
        return self.get_element(self.NAME_BOX, self.get_checkout_form())

    def get_email_box(self):
        return self.get_element(self.EMAIL_BOX, self.get_checkout_form())

    def get_phone_box(self):
        return self.get_element(self.PHONE_BOX, self.get_checkout_form())

    def get_company_box(self):
        return self.get_element(self.COMPANY_BOX, self.get_checkout_form())

    def get_delivery_time_select(self):
        return self.get_element(self.DELIVERY_TIME, self.get_checkout_form())

    def get_remarks_area(self):
        return self.get_element(self.REMARKS_AREA, self.get_checkout_form())

    def get_payment_buttons(self):
        return self.get_elements(self.PAYMENT_BUTTONS, self.get_checkout_form())

    def get_payment_button(self, payment_name):
        payment_list = self.get_payment_buttons()
        for payment in payment_list:
            if payment.text.lower() == payment_name.lower():
                return payment

    def select_ideal_bank_name(self, bank_name):
        bank_select = self.get_element(self.BANK_SELECT_FOR_IDEAL)
        bank_list = self.get_elements(self.BANK_OPTION, bank_select)
        for bank in bank_list:
            if bank.text == bank_name:
                bank.click()
                return

    def select_cash_payment(self, locale):
        self.get_payment_button(self.CASH_PAYMENT[locale]).click()

    def fill_form_data(self, elem, text):
        self.logger.info("Sending Keys: {} to {}".format(text, elem.id))
        elem.send_keys(text)

    def fill_form(self):
        self.fill_form_data(self.get_address_box(), "House No 8")
        self.fill_form_data(self.get_city_box(), "Tahiti")
        self.fill_form_data(self.get_name_box(), "Phil Coulson")
        self.fill_form_data(self.get_email_box(), "phil@avengers.com")
        self.fill_form_data(self.get_phone_box(), "911-888-8888")
        self.fill_form_data(self.get_remarks_area(), "This is a Multiline Remark\nLine 2\nIt is a Beautiful Place")

    def get_order_button(self):
        return self.get_element(self.PAYMENT_ORDER_BUTTON)

    def click_payment_retry_button(self):
        self.wait_for_clickable(self.FAILED_PAYMENT_RETRY_BUTTON)
        self.get_element(self.FAILED_PAYMENT_RETRY_BUTTON).click()
