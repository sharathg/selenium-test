from pages.base import BasePage
from selenium.webdriver.common.by import By


class ICart(BasePage):

    # ===================
    # Inherited Constants
    # ===================
    driver = None
    logger = None

    # ========
    # Locators
    # ========
    BASKET_CONTAINER = (By.ID, "ibasket")
    PRODUCTS_SECTION = (By.ID, "products")
    PRODUCT_ITEM_ELEM = (By.CLASS_NAME, "cart-single-meal")
    PRODUCT_EDIT_BUTTON = (By.CLASS_NAME, "cart-meal-edit-comment")
    PRODUCT_COMMENT = (By.CLASS_NAME, "cart-meal-comment")
    PRODUCT_COMMENT_EDIT_BOX = (By.CLASS_NAME, "cart-meal-textarea")
    EDIT_BOX_ACTIONS = (By.CLASS_NAME, "cart-meal-btns")
    EDIT_BOX_ACTION_ADD = (By.CLASS_NAME, "add")
    PURCHASE_BUTTON = (By.CLASS_NAME, "cartbutton-button")

    # ============
    # Page Methods
    # ============
    def get_basket_container(self):
        return self.get_element(self.BASKET_CONTAINER)

    def get_products_section(self):
        return self.get_element(self.PRODUCTS_SECTION, self.get_basket_container())

    def get_product_elem(self):
        return self.get_element(self.PRODUCT_ITEM_ELEM, self.get_products_section())

    def get_product_edit_button(self):
        return self.get_element(self.PRODUCT_EDIT_BUTTON, self.get_product_elem())

    def get_comment_edit_text_area(self):
        return self.get_element(self.PRODUCT_COMMENT_EDIT_BOX, self.get_product_elem())

    def type_comment(self, text):
        text_area = self.get_comment_edit_text_area()
        self.logger.info("Typing Text: {} to the Comment Edit Button".format(text))
        text_area.send_keys(text)

    def get_product_comment_display(self):
        return self.get_element(self.PRODUCT_COMMENT, self.get_product_elem())

    def get_add_comment_button(self):
        return self.get_element(self.EDIT_BOX_ACTION_ADD, self.get_product_elem())

    def add_comment_to_product(self, text):
        self.get_product_edit_button().click()
        self.type_comment(text)
        self.get_add_comment_button().click()

    def get_purchase_button(self):
        return self.get_element(self.PURCHASE_BUTTON, self.get_basket_container())
