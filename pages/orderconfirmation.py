from pages.base import BasePage
from selenium.webdriver.common.by import By


class OrderConfirmationPage(BasePage):

    # ===================
    # Inherited Constants
    # ===================
    driver = None
    logger = None

    # ========
    # Locators
    # ========
    RESTAURANT_TEXT = (By.CLASS_NAME, "ordersummary__title")
    ORDER_ID = (By.CLASS_NAME, "order-reference-text")

    # ============
    # Page Methods
    # ============
    def get_order_restaurant_name(self):
        return self.get_element(self.RESTAURANT_TEXT).text

    def get_order_id(self):
        return self.get_element(self.ORDER_ID).text.split(":")[-1]