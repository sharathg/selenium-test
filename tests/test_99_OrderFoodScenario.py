from tests.base import BaseTest
from pages.home import HomePage
from pages.restaurantlist import RestaurantListPage
from pages.restaurant import RestaurantPage
from pages.icart import ICart
from pages.payment import PaymentPage
from pages.bank import BankPage
from pages.orderconfirmation import OrderConfirmationPage


class Test99OrderFoodScenario(
    BaseTest,
    HomePage,
    RestaurantListPage,
    RestaurantPage,
    ICart,
    PaymentPage,
    BankPage,
    OrderConfirmationPage
):

    def setUp(self):
        super().setUp()
        HomePage.open_home_page(self)

    def tearDown(self):
        self.clear_cookies()
        super().tearDown()

    def test_99_OrderFood(self):
        '''
        - Give Address as 8889AA
        - Select QA Restaurant Selenium
        - Add multiple products to your basket
            - Fill your basket with 1x Coke, 1x Duck Breast with Tomato and 1x Pizza Salami
            - Add the following comment ‘no sugar’ to any of the products in your basket
        - Place order with online payment method iDEAL (any bank is OK)
        - Cancel iDEAL order and return to checkout
        - Select cash payment and proceed with your order
        '''
        # Give Address as 8889AA
        HomePage.search_using_test_address(self)
        self.wait_for_new_page_load(3)
        self.assertTrue(RestaurantListPage.is_restaurants_list_page(self), "Check if the Restaurant List Page is loaded")
        # Select QA Restaurant Selenium
        RestaurantListPage.get_qa_restaurant(self).click()
        self.wait_for_new_page_load(3)
        self.assertTrue(RestaurantPage.is_qa_restaurant_page(self), "Check if the Restaurant Page is loaded")
        # Add multiple products to your basket
        self.cart_amount = RestaurantPage.get_cart_amount(self)
        self.cart_price = RestaurantPage.get_cart_price(self)
        self.assertEqual(self.cart_amount, 0, "Check that the Cart is Empty")
        self.assertEqual(self.cart_price, 0.0, "Check that the Cart Price is 0")
        # Fill your basket with 1x Coke, 1x Duck Breast with Tomato and 1x Pizza Salami
        duck_price = RestaurantPage.click_menu_tab_item_duck_breast(self)
        duck_price += RestaurantPage.check_menu_tab_item_tomato_checkbox(self)
        duck_price += RestaurantPage.select_menu_teb_item_coke(self)
        add_to_cart_btn_price = RestaurantPage.add_to_cart_item_duck_breast(self)
        self.assertEqual(add_to_cart_btn_price, duck_price, "Make Sure that the Duck Price is as per the web page")
        self.cart_price += duck_price
        self.cart_amount += 1
        self.assertEqual(RestaurantPage.get_cart_amount(self), self.cart_amount, "Check that Cart Amount is Updated")
        self.assertEqual(RestaurantPage.get_cart_price(self), self.cart_price, "Check that Cart Price is Updated")
        self.cart_price += RestaurantPage.click_menu_tab_item_salami(self)
        self.cart_amount += 1
        self.assertEqual(RestaurantPage.get_cart_amount(self), self.cart_amount, "Check that Cart Amount is Updated")
        self.assertEqual(RestaurantPage.get_cart_price(self), self.cart_price, "Check that Cart Price is Updated")
        # Add the following comment ‘no sugar’ to any of the products in your basket
        RestaurantPage.get_cart(self).click()
        ICart.add_comment_to_product(self, "no sugar")
        self.assertEqual(ICart.get_product_comment_display(self).text, "no sugar", "Check that the Comment is updated")
        # Purchase
        ICart.get_purchase_button(self).click()
        self.wait_for_new_page_load(3)
        self.assertTrue(PaymentPage.is_payment_page(self), "Check if the payment page is loaded.")
        self.assertEqual(PaymentPage.get_postcode_box(self).get_attribute('value'), PaymentPage.TEST_ADDRESS,
                         "Check if the PostCode Box is already filled.")
        # Fill Rest of the Test Data
        PaymentPage.fill_form(self)
        # Select iDEAL as the payment and ABN AMRO as bank
        PaymentPage.get_payment_button(self, "iDEAL").click()
        PaymentPage.select_ideal_bank_name(self, "ABN AMRO")
        PaymentPage.get_order_button(self).click()
        self.wait_for_new_page_load(3)
        # Cancel Bank Payment
        BankPage.cancel_bank_payment(self)
        self.wait_for_new_page_load(5)
        # Retry Payment and Pay using Cash
        PaymentPage.click_payment_retry_button(self)
        self.wait_for_new_page_load(3)
        PaymentPage.select_cash_payment(self, HomePage.get_current_locale(self).lower())
        PaymentPage.get_order_button(self).click()
        self.wait_for_new_page_load(3)
        self.assertEqual(OrderConfirmationPage.get_order_restaurant_name(self),
                         RestaurantListPage.TEST_RESTAURANT_NAME,
                         "Check if the Restaurant Name is correct")
        self.logger.info("Order ID: {}".format(OrderConfirmationPage.get_order_id(self)))
