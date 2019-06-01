from tests.base import BaseTest
from pages.restaurantlist import RestaurantListPage


class Test02RestaurantsList(
    BaseTest,
    RestaurantListPage
):

    def setUp(self):
        super().setUp()
        RestaurantListPage.open_restaurants_list_page(self)

    def tearDown(self):
        self.clear_cookies()
        super().tearDown()

    def test_02_01_RestaurantsListPageBasicView(self):
        '''
        Check if the Title contains Test Zip Code
        Check if there is a Location Drop Down
        Check if there is Kitchen Types List
        Check if there is a Filter Menu
        Check if there is a Restaurants List Container
        '''
        self.assertIn(RestaurantListPage.TEST_ZIPCODE, self.title(),
                      "Check that the Title contains {}".format(RestaurantListPage.TEST_ZIPCODE))
        self.assertIsNotNone(RestaurantListPage.get_location_drop_down(self),
                             "Check that there is a Location Drop Down")
        self.assertIsNotNone(RestaurantListPage.get_kitchen_types_container(self),
                             "Check that there is a Kitchen Type Selection Container")
        self.assertIsNotNone(RestaurantListPage.get_filter_sidebar(self),
                             "Check that there is a Filter Sidebar")
        self.assertIsNotNone(RestaurantListPage.get_restaurant_list_container(self),
                             "Check that there is a List for Restaurants")

    def test_02_02_RestaurantsListView(self):
        '''
        Check that there is a list of Restaurants Shown
        Check that the Restaurant Elem in the list has:
            - Logo Wrapper
            - Details Wrapper
        '''
        restaurant_list = RestaurantListPage.get_restaurants_list(self)
        self.assertNotEqual(restaurant_list, [], "Check that the Restaurant List is not Empty")
        qa_restaurant = RestaurantListPage.get_qa_restaurant(self)
        self.assertIsNotNone(qa_restaurant,
                             "Check that the '{}' exists in the restaurant list".format(
                                 RestaurantListPage.TEST_RESTAURANT_NAME))
        self.assertIsNotNone(RestaurantListPage.get_logo_wrapper(self, qa_restaurant),
                             "Check that the restaurant has a Logo Wrapper")
        self.assertIsNotNone(RestaurantListPage.get_details_wrapper(self, qa_restaurant),
                             "Check that the restaurant has a Details Wrapper")

    def test_02_03_ClickOnRestaurant(self):
        '''
        Check that Clicking on the Restaurant takes the user to the Restaurant Page
        '''
        RestaurantListPage.get_qa_restaurant(self).click()
        self.wait_for_new_page_load(3)
        self.assertEqual(self.current_url(), RestaurantListPage.TEST_RESTAURANT_URL,
                         "Check that the URL is changed to the URL for '{}'".format(
                             RestaurantListPage.TEST_RESTAURANT_NAME))
