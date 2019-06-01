import unittest
import xmlrunner

from os import environ


# Home Page Tests
from tests.test_01_HomePage import Test01HomePage

# Restaurants List Tests
from tests.test_02_RestaurantsList import Test02RestaurantsList

# Test Scenario for Ordering Food
from tests.test_99_OrderFoodScenario import Test99OrderFoodScenario


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports',
                                                     outsuffix="Test-{}".format(environ.get('BROWSER', "chrome"))))
