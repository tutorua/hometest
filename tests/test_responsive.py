import pytest
from pages.home_page import HomePage
from config.mobile_devices import MOBILE_DEVICES
from utilities.driver_factory import DriverFactory


class TestResponsiveDesign:
    
    def test_header_responsive(self, driver_init, mobile_helpers):
        """Test if header elements are properly displayed on mobile"""
        home_page = HomePage(driver_init)
        
        # Check if mobile menu button is visible
        assert home_page.is_mobile_menu_visible()
        
        # Check if header fits within viewport
        header_info = mobile_helpers.check_responsive_element(home_page.header)
        assert header_info["within_viewport"]
    
    @pytest.mark.parametrize("device", ["iPhone 12 Pro", "Samsung Galaxy S21", "iPad"])
    def test_cross_device_compatibility(self, device):
        """Test across different mobile devices"""
        driver = DriverFactory.create_mobile_driver(device)
        home_page = HomePage(driver)
        
        # Test basic functionality across devices
        assert home_page.is_page_loaded()
        driver.quit()
    
    def test_touch_interactions(self, driver_init, mobile_helpers):
        """Test mobile-specific touch interactions"""
        home_page = HomePage(driver_init)
        
        # Test tap interaction
        mobile_helpers.tap(home_page.menu_button)
        assert home_page.is_menu_expanded()
        
        # Test swipe interaction
        mobile_helpers.swipe_left(home_page.carousel)
        # Add assertions for swipe behavior
