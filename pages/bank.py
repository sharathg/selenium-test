from pages.base import BasePage
from selenium.webdriver.common.by import By


class BankPage(BasePage):

    # ===================
    # Inherited Constants
    # ===================
    driver = None
    logger = None

    # ========
    # Locators
    # ========
    BANK_CANCEL_BUTTON = (By.CLASS_NAME, "ocf-btn-cancel")
    BANK_CANCEL_ACCEPT_BUTTON = (By.CLASS_NAME, "btn-primary")
    COOKIE_ACCEPT_BUTTON = (By.CLASS_NAME, "mlf-buttons-right")

    # ============
    # Page Methods
    # ============
    def cancel_bank_payment(self):
        try:
            self.get_element(self.COOKIE_ACCEPT_BUTTON, timeout=3).click()
        except Exception as e:
            self.logger.info(e)
        self.get_element(self.BANK_CANCEL_BUTTON).click()
        self.get_element(self.BANK_CANCEL_ACCEPT_BUTTON).click()
