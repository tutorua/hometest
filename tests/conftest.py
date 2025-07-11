import pytest
import os
from datetime import datetime
from utilities.driver_factory import DriverFactory
from config.settings import BASE_URL, SCREENSHOTS_DIR
from utilities.mobile_helpers import MobileHelpers

@pytest.fixture(scope="session")
def driver_init(request):
    """Initialize driver for the test session"""
    device = request.config.getoption("--device", default=None)
    driver = DriverFactory.create_mobile_driver(device)
    driver.get(BASE_URL)
    yield driver
    driver.quit()

@pytest.fixture
def mobile_helpers(driver_init):
    """Provide mobile helper utilities"""
    return MobileHelpers(driver_init)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver_init')
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = SCREENSHOTS_DIR / screenshot_name
            
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            driver.save_screenshot(str(screenshot_path))
            print(f"Screenshot saved: {screenshot_path}")

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption("--device", action="store", default=None, 
                     help="Mobile device to emulate (defaults to settings.DEFAULT_MOBILE_DEVICE)")
    parser.addoption("--headless", action="store_true", 
                     help="Run tests in headless mode")
    