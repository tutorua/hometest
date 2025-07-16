from selenium.webdriver.common.action_chains import ActionChains


class MobileHelpers:
    
    def __init__(self, driver):
        self.driver = driver
    
    def tap(self, element):
        """Simulate mobile tap"""
        ActionChains(self.driver).click(element).perform()
    
    def long_press(self, element, duration=2):
        """Simulate long press"""
        ActionChains(self.driver).click_and_hold(element).pause(duration).release().perform()
    
    def swipe_left(self, element):
        """Swipe left on element"""
        action = ActionChains(self.driver)
        action.click_and_hold(element).move_by_offset(-100, 0).release().perform()
    
    def swipe_right(self, element):
        """Swipe right on element"""
        action = ActionChains(self.driver)
        action.click_and_hold(element).move_by_offset(100, 0).release().perform()
    
    def check_responsive_element(self, element):
        """Check if element is properly sized for mobile"""
        size = element.size
        location = element.location
        
        # Check if element is within viewport
        viewport_width = self.driver.execute_script("return window.innerWidth;")
        viewport_height = self.driver.execute_script("return window.innerHeight;")
        
        return {
            "width": size["width"],
            "height": size["height"],
            "x": location["x"],
            "y": location["y"],
            "within_viewport": (
                location["x"] >= 0 and 
                location["y"] >= 0 and 
                location["x"] + size["width"] <= viewport_width and
                location["y"] + size["height"] <= viewport_height
            )
        }
    
    def get_viewport_size(self):
        """Get current viewport dimensions"""
        width = self.driver.execute_script("return window.innerWidth;")
        height = self.driver.execute_script("return window.innerHeight;")
        return {"width": width, "height": height}


    def take_screenshot(self, screenshot_path):
        """Save a screenshot of the current view"""
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
