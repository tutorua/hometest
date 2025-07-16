import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from config.mobile_devices import MOBILE_DEVICES
from utilities.mobile_helpers import MobileHelpers
from config.settings import SCREENSHOTS_DIR
from utilities.general import General

class TestResponsiveDesign:

    @pytest.mark.responsive
    def test_bottom_menu_displayed(self, driver_init):
        """Test if the bottom menu is displayed on mobile"""
        home_page = HomePage(driver_init)
        assert home_page.is_mobile_menu_visible()


    @pytest.mark.responsive
    def test_touch_interactions(self, driver_init, request):
        """Test the Search form interactions on mobile"""

        test_name = request.node.name  # Get current test name
        search_text = "StarCraftII"
        home_page = HomePage(driver_init)
        home_page.click(home_page.menu_browse)
        input_field = home_page.driver.find_element(By.CSS_SELECTOR, home_page.CSS_SEARCH)
        input_field.click()
        input_field.send_keys(search_text)
        # item = WebDriverWait(home_page.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li:nth-child(2)")))
        item = WebDriverWait(home_page.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul > li:nth-child(2)")))
        item.click()
        top_video = home_page.driver.find_element(By.CSS_SELECTOR,"img.tw-image")
        top_video.click()
        # Make sure the page with video have been loaded
        WebDriverWait(home_page.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "Welcome to the chat room!")]'))
        )
        # Take screenshot after interaction
        driver_init.save_screenshot(SCREENSHOTS_DIR / f"{test_name}.png")
        video = '//*[@id="channel-live-overlay"]/div/div/div[1]/div/div/div/div[2]/video'
        # Assert the video is playing (not paused) That approach might not work for Twitch
        # is_playing = driver_init.execute_script("return arguments[0].paused === false;", video)
        # assert is_playing, "Video is not playing"
        # Wait for the element to be visible
        time_elem = WebDriverWait(home_page.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Time Spent Live Streaming"]'))
        )

        # Get the initial time
        time1_str = time_elem.text
        time1 = General.parse_time(time1_str)

        # Wait 3 seconds
        time.sleep(3)

        # Get the time again
        time2_str = time_elem.text
        time2 = General.parse_time(time2_str)

        # Assert the difference is greater than 2 seconds
        assert (time2 - time1) > 2, f"Time did not advance as expected: {time1_str} -> {time2_str}"
