from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = (By.CSS_SELECTOR, "header")
        self.menu_button = (By.CSS_SELECTOR, ".menu-button")
        self.mobile_menu = (By.CSS_SELECTOR, ".mobile-menu")
        self.carousel = (By.CSS_SELECTOR, ".carousel")

    def is_mobile_menu_visible(self):
        return self.is_element_visible(self.mobile_menu)

    def is_page_loaded(self):
        return self.is_element_visible(self.header)

    def is_menu_expanded(self):
        return self.is_element_visible(self.mobile_menu)
    