from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from config.settings import DRIVERS_DIR, IMPLICIT_WAIT, DEFAULT_MOBILE_DEVICE
from config.mobile_devices import MOBILE_DEVICES

class DriverFactory:
    
    @staticmethod
    def create_mobile_driver(device_name=None):
        # Use device_name if provided, otherwise fall back to settings default
        device_name = device_name or DEFAULT_MOBILE_DEVICE
        
        chrome_options = Options()
        
        # Mobile emulation settings
        device_config = MOBILE_DEVICES.get(device_name)
        if not device_config:
            raise ValueError(f"Device '{device_name}' not found in MOBILE_DEVICES configuration")
        
        mobile_emulation = {
            "deviceMetrics": {
                "width": device_config["width"],
                "height": device_config["height"],
                "pixelRatio": device_config["pixel_ratio"]
            },
            "userAgent": device_config["user_agent"]
        }
        
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Optional: Run in headless mode
        # chrome_options.add_argument("--headless")
        
        service = Service(str(DRIVERS_DIR / "chromedriver"))
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        
        return driver