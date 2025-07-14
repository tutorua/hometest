import pytest
import os
from datetime import datetime
from utilities.driver_factory import DriverFactory
from config.settings import BASE_URL, SCREENSHOTS_DIR, DEFAULT_BROWSER
from utilities.mobile_helpers import MobileHelpers

@pytest.fixture(scope="session")
def driver_init(request):
    """Initialize driver for the test session"""
    browser = request.config.getoption("--browser", default=DEFAULT_BROWSER)
    device = request.config.getoption("--device", default=None)
    headless = request.config.getoption("--headless", default=False)
    
    # Validate browser choice
    if browser.lower() not in ["chrome", "firefox", "edge"]:
        raise ValueError(f"Unsupported browser: {browser}. Supported browsers are: chrome, firefox, edge.")
    
    # Determine if mobile mode
    is_mobile = device is not None
    
    try:
        if is_mobile:
            print(f"Using mobile device: {device} with browser: {browser}")
            # Use the updated parameter order: browser_name first, then device_name
            driver = DriverFactory.create_mobile_driver(browser, device)
        else:
            print(f"Desktop mode selected with browser: {browser}")
            driver = DriverFactory.create_desktop_driver(browser)
        
        # Apply headless mode if requested (this would need to be implemented in DriverFactory)
        if headless:
            print("Running in headless mode")
            # Note: You'll need to modify DriverFactory to accept headless parameter
            # For now, this is just informational
        
        # Navigate to base URL
        driver.get(BASE_URL)
        
        # Store test configuration for later use
        driver._test_config = {
            'browser': browser,
            'device': device,
            'headless': headless,
            'is_mobile': is_mobile
        }
        
        yield driver
        
    except Exception as e:
        print(f"Failed to initialize driver: {e}")
        raise
    finally:
        if 'driver' in locals() and driver:
            driver.quit()


@pytest.fixture
def mobile_helpers(driver_init):
    """Provide mobile helper utilities"""
    return MobileHelpers(driver_init)


@pytest.fixture
def is_mobile(driver_init):
    """Check if current test is running in mobile mode"""
    return getattr(driver_init, '_test_config', {}).get('is_mobile', False)


@pytest.fixture
def current_browser(driver_init):
    """Get current browser name"""
    return getattr(driver_init, '_test_config', {}).get('browser', DEFAULT_BROWSER)


@pytest.fixture
def current_device(driver_init):
    """Get current device name (None for desktop)"""
    return getattr(driver_init, '_test_config', {}).get('device', None)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver_init')
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Get test configuration for better screenshot naming
            test_config = getattr(driver, '_test_config', {})
            browser = test_config.get('browser', 'unknown')
            device = test_config.get('device', 'desktop')
            
            screenshot_name = f"{item.name}_{browser}_{device}_{timestamp}.png"
            screenshot_path = SCREENSHOTS_DIR / screenshot_name
            
            # Ensure screenshots directory exists
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            
            try:
                driver.save_screenshot(str(screenshot_path))
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Failed to save screenshot: {e}")


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser", 
        action="store", 
        default=DEFAULT_BROWSER,
        help="Browser to use for tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--device", 
        action="store", 
        default=None, 
        help="Mobile device to emulate (defaults to settings.DEFAULT_MOBILE_DEVICE)"
    )
    parser.addoption(
        "--headless", 
        action="store_true", 
        help="Run tests in headless mode"
    )


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "mobile: mark test as mobile-specific"
    )
    config.addinivalue_line(
        "markers", "desktop: mark test as desktop-specific"
    )
    config.addinivalue_line(
        "markers", "browser(name): mark test for specific browser"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on runtime configuration"""
    device = config.getoption("--device")
    browser = config.getoption("--browser")
    
    skip_mobile = pytest.mark.skip(reason="Mobile device not specified")
    skip_desktop = pytest.mark.skip(reason="Desktop mode not compatible")
    skip_browser = pytest.mark.skip(reason=f"Test not compatible with {browser}")
    
    for item in items:
        # Skip mobile tests if no device specified
        if "mobile" in item.keywords and not device:
            item.add_marker(skip_mobile)
        
        # Skip desktop tests if mobile device specified
        if "desktop" in item.keywords and device:
            item.add_marker(skip_desktop)
        
        # Skip browser-specific tests
        if "browser" in item.keywords:
            browser_markers = [mark for mark in item.iter_markers(name="browser")]
            if browser_markers:
                supported_browsers = [mark.args[0] for mark in browser_markers]
                if browser.lower() not in [b.lower() for b in supported_browsers]:
                    item.add_marker(skip_browser)