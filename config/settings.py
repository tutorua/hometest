import os
from pathlib import Path
from datetime import datetime

# Base configurations
BASE_URL = "https://m.twitch.tv/"
DEFAULT_BROWSER = "chrome"
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 20
SCREENSHOT_ON_FAILURE = True

# Mobile configurations
DEFAULT_MOBILE_DEVICE = "iPhone 12 Pro"
MOBILE_VIEWPORT_WIDTH = 375
MOBILE_VIEWPORT_HEIGHT = 812

# Paths
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots" / timestamp
if not SCREENSHOTS_DIR.exists():
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = PROJECT_ROOT / "reports"
DRIVERS_DIR = PROJECT_ROOT / "drivers"
LOGS_DIR = PROJECT_ROOT / "logs"
