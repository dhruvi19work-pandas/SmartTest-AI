import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
BASE_URL = os.getenv('BASE_URL', 'https://the-internet.herokuapp.com').rstrip('/')
BROWSER = os.getenv('BROWSER', 'chromium')
BROWSER_CHANNEL = os.getenv('BROWSER_CHANNEL') or None
HEADLESS = os.getenv('HEADLESS', 'true').lower() in {'1', 'true', 'yes'}
SLOW_MO = int(os.getenv('SLOW_MO', '0'))
