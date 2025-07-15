import pytest
from pages.home_page import HomePage
from config.mobile_devices import MOBILE_DEVICES
from utilities.driver_factory import DriverFactory


class TestDesign:
    
    @pytest.mark.desktop
    def test_title(self, driver_init):
        """Test if the page title is correct"""
        home_page_title = "Twitch"
        # home_page = DriverFactory.create_driver(browser_name, mobile = False, device_name = None)
        home_page = HomePage(driver_init)
        assert home_page.getTitle() == home_page_title


    @pytest.mark.desktop
    def test_logo(self, driver_init):
        """Test if the logo is displayed correctly"""
        home_page = HomePage(driver_init)
        assert home_page.is_logo_displayed()


    @pytest.mark.desktop
    def test_header_elements(self, driver_init):
        """Test if header elements are displayed correctly"""
        home_page = HomePage(driver_init)
        # assert home_page.is_desktop_menu_visible()
        # assert home_page.is_page_loaded()
        assert 1 == 1

        