from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):

    CSS_logo = "a>div.tw-svg"


    def __init__(self, driver):
        super().__init__(driver)
        self.header = (By.CSS_SELECTOR, "header")
        self.menu_button = (By.CSS_SELECTOR, ".menu-button")
        self.mobile_menu = (By.CSS_SELECTOR, ".mobile-menu")
        self.carousel = (By.CSS_SELECTOR, ".carousel")

    def is_mobile_menu_visible(self):
        return self.is_element_visible(self.mobile_menu)
    
    def is_desktop_menu_visible(self):
        return self.is_element_visible(self.menu_button)

    def is_page_loaded(self):
        return self.is_element_visible(self.header)

    def is_menu_expanded(self):
        return self.is_element_visible(self.mobile_menu)
    
    def getTitle(self):
        return self.driver.title
    
    def is_logo_displayed(self):
        logo = self.driver.find_element("css selector", self.CSS_logo)
        return logo.is_displayed()