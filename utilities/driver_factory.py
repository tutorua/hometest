from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from config.settings import DRIVERS_DIR, IMPLICIT_WAIT, DEFAULT_MOBILE_DEVICE
from config.mobile_devices import MOBILE_DEVICES

class DriverFactory:

    @staticmethod
    def mobile_chrome_driver(device_name: str):
        """Create a mobile Chrome driver with device emulation."""
        chrome_options = ChromeOptions()
        
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
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # Optional: Run in headless mode
        # chrome_options.add_argument("--headless")
        
        try:
            service_chr = ChromeService(str(DRIVERS_DIR / "chromedriver"))
            driver = webdriver.Chrome(service=service_chr, options=chrome_options)
            driver.implicitly_wait(IMPLICIT_WAIT)
            return driver
        except WebDriverException as e:
            raise RuntimeError(f"Failed to initialize mobile Chrome driver: {e}")


    @staticmethod
    def mobile_firefox_driver(device_name: str):
        """Create a pseudo-mobile Firefox driver with device emulation."""
        firefox_options = FirefoxOptions()
        
        # Mobile emulation settings
        device_config = MOBILE_DEVICES.get(device_name)
        if not device_config:
            raise ValueError(f"Device '{device_name}' not found in MOBILE_DEVICES configuration")
        
        # Set user agent
        firefox_options.set_preference("general.useragent.override", device_config["user_agent"])
        
        # Set viewport size (Firefox doesn't have exact mobile emulation like Chrome)
        firefox_options.set_preference("layout.css.devPixelsPerPx", str(device_config["pixel_ratio"]))
        
        # Enable responsive design mode
        firefox_options.set_preference("devtools.responsive.metaViewport.enabled", True)
        
        # Optional: Run in headless mode
        # firefox_options.add_argument("--headless")
        
        try:
            service_ff = FirefoxService(str(DRIVERS_DIR / "geckodriver"))
            driver = webdriver.Firefox(service=service_ff, options=firefox_options)
            
            # Set window size to simulate mobile device
            driver.set_window_size(device_config["width"], device_config["height"])
            driver.implicitly_wait(IMPLICIT_WAIT)
            return driver
        except WebDriverException as e:
            raise RuntimeError(f"Failed to initialize mobile Firefox driver: {e}")


    @staticmethod
    def mobile_edge_driver(device_name: str):
        """Create a mobile Edge driver with device emulation."""
        edge_options = EdgeOptions()
        
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
        
        edge_options.add_experimental_option("mobileEmulation", mobile_emulation)
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--disable-web-security")
        edge_options.add_argument("--allow-running-insecure-content")
        
        # Optional: Run in headless mode
        # edge_options.add_argument("--headless")
        
        try:
            service_edge = EdgeService(str(DRIVERS_DIR / "msedgedriver"))
            driver = webdriver.Edge(service=service_edge, options=edge_options)
            driver.implicitly_wait(IMPLICIT_WAIT)
            return driver
        except WebDriverException as e:
            raise RuntimeError(f"Failed to initialize mobile Edge driver: {e}")


    @staticmethod
    def create_mobile_driver(browser_name: str, device_name=None):
        """Create a mobile driver for the specified browser and device."""
        # Use device_name if provided, otherwise fall back to settings default
        device_name = device_name or DEFAULT_MOBILE_DEVICE
        
        if browser_name.lower() == "chrome":
            driver = DriverFactory.mobile_chrome_driver(device_name)
        elif browser_name.lower() == "firefox":
            driver = DriverFactory.mobile_firefox_driver(device_name)
        elif browser_name.lower() == "edge":
            driver = DriverFactory.mobile_edge_driver(device_name)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}. Supported browsers are: chrome, firefox, edge.")
        
        return driver


    @staticmethod
    def create_desktop_driver(browser_name: str):
        """Create a desktop driver for the specified browser."""
        try:
            if browser_name.lower() == "chrome":
                chrome_options = ChromeOptions()
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--start-maximized")
                service = ChromeService(str(DRIVERS_DIR / "chromedriver"))
                driver = webdriver.Chrome(service=service, options=chrome_options)           
            elif browser_name.lower() == "firefox":
                firefox_options = FirefoxOptions()
                # Add any Firefox-specific options here if needed
                service = FirefoxService(str(DRIVERS_DIR / "geckodriver"))
                driver = webdriver.Firefox(service=service, options=firefox_options)
                driver.maximize_window()            
            elif browser_name.lower() == "edge":
                edge_options = EdgeOptions()
                edge_options.add_argument("--no-sandbox")
                edge_options.add_argument("--disable-dev-shm-usage")
                edge_options.add_argument("--disable-gpu")
                edge_options.add_argument("--start-maximized")
                service = EdgeService(str(DRIVERS_DIR / "msedgedriver"))
                driver = webdriver.Edge(service=service, options=edge_options)               
            else:
                raise ValueError(f"Unsupported browser: {browser_name}. Supported browsers are: chrome, firefox, edge.")
            
            driver.implicitly_wait(IMPLICIT_WAIT)
            return driver
            
        except WebDriverException as e:
            raise RuntimeError(f"Failed to initialize the {browser_name} driver: {e}")


    @staticmethod
    def create_driver(browser_name: str, mobile: bool = False, device_name = None):
        """
        Factory method to create either desktop or mobile driver.
        
        Args:
            browser_name (str): Name of the browser (chrome, firefox, edge)
            mobile (bool): Whether to create a mobile driver
            device_name (str): Device name for mobile emulation (optional)
            
        Returns:
            driver: Configured WebDriver instance
        """
        if mobile:
            driver = DriverFactory.create_mobile_driver(browser_name, device_name)
        else:
            driver = DriverFactory.create_desktop_driver(browser_name)
        
        return driver