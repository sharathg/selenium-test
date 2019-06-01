from tests.base import BaseTest
from pages.home import HomePage


class Test01HomePage(
    BaseTest,
    HomePage
):

    def setUp(self):
        super().setUp()
        HomePage.open_home_page(self)

    def tearDown(self):
        self.clear_cookies()
        super().tearDown()

    def test_01_01_HomePageBasicView(self):
        '''
        Check if the Title contains Thuisbezorgd
        Check that current locale is NL
        Check that there is a delivery area form with: Text Box, Submit Button present
        Also Check that there is an AutoComplete Drop Down which is not displayed
        '''
        self.assertIn(HomePage.TITLE.lower(), self.title().lower(), "Check if Title contains {}".format(HomePage.TITLE))
        self.assertEqual(HomePage.get_current_locale(self).lower(), HomePage.DEFAULT_LOCALE.lower(),
                         "Check that current locale is {}".format(HomePage.DEFAULT_LOCALE))
        delivery_area_form = HomePage.get_delivery_area_form(self)
        self.assertIsNotNone(delivery_area_form, "Check Delivery Area Form exists")
        self.assertIsNotNone(HomePage.get_address_text_box(self, delivery_area_form), "Check Address Text Box exists")
        self.assertIsNotNone(HomePage.get_submit_button(self, delivery_area_form), "Check Submit Button exists")
        self.assertFalse(HomePage.get_autocomplete_drop_down(self, delivery_area_form).is_displayed(),
                         "Check that the AutoComplete Drop Down is not Displayed by Default")

    def test_01_02_ChangeLocale(self):
        '''
        Check that Locale of the Page can be changed
        Check that the Locale can be set to EN
        Check that setting the locale to EN will change the current URL
        Check that the locale setting flag also changes to EN
        Check that the Locale can be set to DE
        Check that setting the locale to DE will change the current URL
        Check that the locale setting flag also changes to DE
        '''
        HomePage.change_locale(self, 'en')
        self.assertEqual(HomePage.get_current_locale(self).lower(), 'en', "Check that changed locale Flag is EN")
        self.assertEqual(self.driver.current_url, "{}/en/".format(HomePage.HOME_PAGE_URL), "Check if URL is for EN.")
        HomePage.change_locale(self, 'de')
        self.assertEqual(HomePage.get_current_locale(self).lower(), 'de', "Check that changed locale Flag is DE")
        self.assertEqual(self.driver.current_url, "{}/de/".format(HomePage.HOME_PAGE_URL), "Check if URL is for DE.")

    def test_01_03_DeliveryAreaForm(self):
        '''
        Check that Typing anything in the address box opens the AutoComplete Drop Down
        Check that When the DropDown is present, Submit Button is not visible
        Check that the AddressBox can be cleared
        Type in text and Click outside the Text Box, The AutoComplete Drop Down should disappear
            And the Submit Button should be displayed
        '''
        HomePage.type_in_address_box(self, "888")
        HomePage.wait_for_drop_down(self)
        self.assertTrue(HomePage.get_autocomplete_drop_down(self).is_displayed(),
                        "Check that the AutoComplete Drop Down is now Displayed")
        self.assertFalse(HomePage.get_submit_button(self).is_displayed(),
                         "Check that the Submit Button is not Displayed")
        HomePage.clear_address_box(self)
        self.assertEqual(HomePage.get_address_box_value(self), "",
                         "Check that the Address Box Value is Empty")
        HomePage.type_in_address_box(self, "888")
        HomePage.wait_for_drop_down(self)
        self.assertTrue(HomePage.get_autocomplete_drop_down(self).is_displayed(),
                        "Check that the AutoComplete Drop Down is now Displayed")
        HomePage.click_outside_address_box(self)
        self.assertFalse(HomePage.get_autocomplete_drop_down(self).is_displayed(),
                         "Check that the AutoComplete Drop Down is NOT Displayed")
        self.assertTrue(HomePage.get_submit_button(self).is_displayed(),
                        "Check that the Submit Button is now Displayed")

    def test_01_04_SearchTestRestaurantsByClickingTheSubmitButton(self):
        '''
        Check that Typing the Test Address and Clicking on the Submit Button,
            takes the user to the Restaurants List
        '''
        HomePage.type_in_address_box(self, self.TEST_ADDRESS)
        HomePage.click_outside_address_box(self)
        HomePage.get_submit_button(self).click()
        self.wait_for_new_page_load()
        self.assertEqual(self.current_url(), HomePage.TEST_RESTAURANTS_LIST_URL,
                         "Check that the URL is changed to the URL for Restaurants List")

    def test_01_05_SearchTestRestaurantsByTypingEnterInSearchBox(self):
        '''
        Check that Typing the Test Address and Pressing ENTER,
            takes the user to the Restaurants List
        '''
        HomePage.type_in_address_box(self, self.TEST_ADDRESS)
        HomePage.press_enter_in_address_box(self)
        self.wait_for_new_page_load()
        self.assertEqual(self.current_url(), HomePage.TEST_RESTAURANTS_LIST_URL,
                         "Check that the URL is changed to the URL for Restaurants List")
