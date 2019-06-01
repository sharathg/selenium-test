from pages.base import BasePage
from selenium.webdriver.common.by import By


class RestaurantPage(BasePage):

    # ===================
    # Inherited Constants
    # ===================
    driver = None
    logger = None

    # =========
    # Test Data
    # =========
    QA_RESTAURANT_URL = "https://www.thuisbezorgd.nl/qa-restaurant-selenium"
    TEST_ADDRESS = "ENSCHEDE, 8889AA"
    QA_RESTAURANT_NAME = "QA Restaurant Selenium"

    # ========
    # Locators
    # ========
    DROP_DOWN_LOCATION = (By.ID, "dropdown-location")
    RESTAURANT_NAME_HEADER = (By.CLASS_NAME, "title-delivery")
    BACK_TO_LIST = (By.CLASS_NAME, "go-back-button")
    BASKET_BUTTON = (By.ID, "btn-basket")
    BASKET_PRICE = (By.CLASS_NAME, "btn-cart-price")
    BASKET_AMOUNT = (By.CLASS_NAME, "btn-cart-amount")
    MENU_CATEGORY_LIST = (By.CLASS_NAME, "menu-category-list")
    MENU_CATEGORY_ITEM = (By.TAG_NAME, "a")
    MENU_TAB_CONTENT = (By.ID, "menu-tab-content")
    MENU_TAB_CATEGORY = (By.CLASS_NAME, "menucard__meals-group")
    MENU_TAB_ITEM = (By.CLASS_NAME, "meal")
    MENU_TAB_ITEM_NAME = (By.CLASS_NAME, "meal-name")
    MENU_TAB_ITEM_PRICE = (By.CLASS_NAME, "meal__price")
    MENU_TAB_ITEM_SIDEDISH_CHECKBOX = (By.CLASS_NAME, "sidedish-checkbox")
    MENU_TAB_ITEM_SIDEDISH_CHECKBOX_INPUT = (By.TAG_NAME, "input")
    MENU_TAB_ITEM_SIDEDISH_LIST = (By.CLASS_NAME, "sidedish-select")
    MENU_TAB_ITEM_SIDEDISH_LIST_OPTION = (By.TAG_NAME, "option")
    MENU_TAB_ITEM_SIDEDISH_ADD_TO_CART = (By.CLASS_NAME, "button_add_value")

    # ============
    # Page Methods
    # ============
    def open_qa_restaurant_page(self):
        self.logger.info("Opening URL: {}".format(self.QA_RESTAURANT_URL))
        self.driver.get(self.QA_RESTAURANT_URL)

    def is_qa_restaurant_page(self):
        return self.get_restaurant_name_header().text == self.QA_RESTAURANT_NAME

    def get_restaurant_name_header(self):
        return self.get_element(self.RESTAURANT_NAME_HEADER)

    def get_back_to_restaurant_list_button(self):
        return self.get_element(self.BACK_TO_LIST)

    def get_cart(self):
        return self.get_element(self.BASKET_BUTTON)

    def get_cart_amount(self):
        return int(self.get_element(self.BASKET_AMOUNT, self.get_cart()).text)

    def get_cart_price(self):
        return self.convert_amount_to_float(self.get_element(self.BASKET_PRICE, self.get_cart()).text)

    def get_menu_category_list(self):
        return self.get_element(self.MENU_CATEGORY_LIST)

    def get_menu_category_item(self, category):
        item_list = self.get_elements(self.MENU_CATEGORY_ITEM, self.get_menu_category_list())
        for item in item_list:
            if category in item.text:
                return item
        return None

    def get_menu_tab_content(self):
        return self.get_element(self.MENU_TAB_CONTENT)

    def get_menu_tab_items(self):
        return self.get_elements(self.MENU_TAB_ITEM)

    def __get_menu_tab_item__(self, item_name):
        item_list = self.get_menu_tab_items()
        for item in item_list:
            if self.get_element(self.MENU_TAB_ITEM_NAME, item).text == item_name:
                return item

    def __click_menu_tab_item__(self, item_name):
        item = self.__get_menu_tab_item__(item_name)
        amount = self.get_element(self.MENU_TAB_ITEM_PRICE, item).text
        item.click()
        self.wait_for_document_ready()
        return self.convert_amount_to_float(amount)

    def click_menu_tab_item_duck_breast(self):
        return self.__click_menu_tab_item__("Duck Breast")

    def add_to_cart_item_duck_breast(self):
        item = self.__get_menu_tab_item__("Duck Breast")
        add_to_cart = self.get_element(self.MENU_TAB_ITEM_SIDEDISH_ADD_TO_CART, item)
        amount = add_to_cart.text
        add_to_cart.click()
        return self.convert_amount_to_float(amount)

    def click_menu_tab_item_salami(self):
        return self.__click_menu_tab_item__("Salami")

    def check_menu_tab_item_tomato_checkbox(self):
        self.wait_for_clickable(self.MENU_TAB_ITEM_SIDEDISH_CHECKBOX)
        check_list = self.get_elements(self.MENU_TAB_ITEM_SIDEDISH_CHECKBOX)
        for check in check_list:
            input_elem = self.get_element(self.MENU_TAB_ITEM_SIDEDISH_CHECKBOX_INPUT, check)
            if input_elem.get_attribute('data-name').lower() == "tomato":
                if not input_elem.is_selected():
                    check.click()
                return float(input_elem.get_attribute('data-price'))

    def select_menu_teb_item_coke(self):
        select_list = self.get_elements(self.MENU_TAB_ITEM_SIDEDISH_LIST_OPTION,
                                        self.get_element(self.MENU_TAB_ITEM_SIDEDISH_LIST))
        for select in select_list:
            if select.text.lower().startswith("coke"):
                if not select.is_selected():
                    select.click()
                return float(select.get_attribute('data-price'))

    def convert_amount_to_float(self, amount):
        new = amount.replace("€ ", "").replace(",", ".")
        new = new.split()[0]
        self.logger.info("Converted Amount: {} To: {}".format(amount, new))
        return float(new)

