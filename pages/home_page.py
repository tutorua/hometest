from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):

    CSS_LOGO = "a>div.tw-svg"
    CSS_FOLLOWING = "#twilight-sticky-header-root > div > div > ul > li:nth-child(1) > a > div > div > div"
    CSS_LIVE = "#twilight-sticky-header-root > div > div > ul > li:nth-child(2) > a > div > div > div"
    CSS_SEARCH = ".tw-input"
    XPATH_HOME = "//div[contains(@class, 'CoreText-sc-1txzju1-0') and text()='Home']"
    XPATH_BROWSE = "//div[contains(@class, 'CoreText-sc-1txzju1-0') and text()='Browse']"
    XPATH_ACTIVITY = "//div[contains(@class, 'CoreText-sc-1txzju1-0') and text()='Activity']"
    XPATH_PROFILE = "//div[contains(@class, 'CoreText-sc-1txzju1-0') and text()='Profile']"


    def __init__(self, driver):
        super().__init__(driver)
        self.logo = (By.CSS_SELECTOR, self.CSS_LOGO)
        self.menu_following = (By.CSS_SELECTOR, self.CSS_FOLLOWING)
        self.menu_live = (By.CSS_SELECTOR, self.CSS_LIVE)
        self.menu_home = (By.XPATH, self.XPATH_HOME)
        self.menu_browse = (By.XPATH, self.XPATH_BROWSE)
        self.menu_activity = (By.XPATH, self.XPATH_ACTIVITY)
        self.menu_profile = (By.XPATH, self.XPATH_PROFILE)        


    def getTitle(self):
        return self.driver.title
    
    def is_mobile_menu_visible(self):
        return self.is_element_visible((By.XPATH, self.XPATH_HOME)) and \
             self.is_element_visible((By.XPATH, self.XPATH_BROWSE)) and \
             self.is_element_visible((By.XPATH, self.XPATH_ACTIVITY)) and \
             self.is_element_visible((By.XPATH, self.XPATH_PROFILE))
       
    def is_logo_displayed(self):
        logo = self.driver.find_element("css selector", self.logo)
        return logo.is_displayed()
    
    def is_browse_visible(self):
        return self.is_element_visible((By.XPATH, self.menu_browse))
    
"""     def save_screenshot(self, file_path):
        self.driver.save_screenshot(file_path)
 """    