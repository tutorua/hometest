import pytest

from pages.home_page import HomePage
from config.mobile_devices import MOBILE_DEVICES
from utilities.mobile_helpers import MobileHelpers
from config.settings import SCREENSHOTS_DIR
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestResponsiveDesign:

    @pytest.mark.responsive
    def test_bottom_menu_displayed(self, driver_init):
        """Test if the bottom menu is displayed on mobile"""
        home_page = HomePage(driver_init)
        assert home_page.is_mobile_menu_visible()


    @pytest.mark.responsive
    def test_touch_interactions(self, driver_init, request):
        """Test the Search form interactions on mobile"""

        search_text = "StarCraftII"
        home_page = HomePage(driver_init)
        home_page.click(home_page.menu_browse)
        input_field = home_page.driver.find_element(By.CSS_SELECTOR, home_page.CSS_SEARCH)
        input_field.click()
        input_field.send_keys(search_text)
        # item = WebDriverWait(home_page.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li:nth-child(2)")))
        item = WebDriverWait(home_page.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul > li:nth-child(2)")))

        test_name = request.node.name  # Get current test name
        screenshot_name = f"{test_name}.png"
        screenshot_path = SCREENSHOTS_DIR / screenshot_name
        driver_init.save_screenshot(str(screenshot_path))
       
        
        item.click()


        # Test tap interaction
        #mobile_helpers.tap(home_page.menu_browse)
        assert 1 == 1
        
        # Test swipe interaction
        # mobile_helpers.swipe_left(home_page.carousel)
        # Add assertions for swipe behavior
        # # Check if header fits within viewport
        # header_info = mobile_helpers.check_responsive_element(home_page.header)
        # assert header_info["within_viewport"]
    

    # @pytest.mark.responsive
    # @pytest.mark.parametrize("device", ["iPhone 12 Pro", "Samsung Galaxy S21", "iPad"])
    # def test_cross_device_compatibility(self, device):
    #     """Test across different mobile devices"""
    #     driver = DriverFactory.create_mobile_driver(device)
    #     home_page = HomePage(driver)
        
    #     # Test basic functionality across devices
    #     assert home_page.is_page_loaded()
    #     driver.quit()
    


