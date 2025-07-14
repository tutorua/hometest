import os
from pathlib import Path

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
PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"
DRIVERS_DIR = PROJECT_ROOT / "drivers"
LOGS_DIR = PROJECT_ROOT / "logs"
