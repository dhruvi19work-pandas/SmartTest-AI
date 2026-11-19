from playwright.sync_api import sync_playwright
from core.logger import get_logger
from config.settings import SLOW_MO

class BrowserManager:
    def __init__(self,browser_name='chromium',headless=True,browser_channel=None):
        self.browser_name=browser_name; self.headless=headless; self.browser_channel=browser_channel
        self.playwright=None; self.browser=None; self.logger=get_logger('BrowserManager')
    def start_browser(self):
        self.playwright=sync_playwright().start()
        try:
            browser_type=getattr(self.playwright,self.browser_name)
            options={'headless':self.headless,'slow_mo':SLOW_MO}
            if self.browser_channel: options['channel']=self.browser_channel
            self.browser=browser_type.launch(**options); self.logger.info('Browser started'); return self.browser
        except Exception:
            self.logger.exception('Browser launch failed'); self.playwright.stop(); self.playwright=None; raise
    def stop_browser(self):
        try:
            if self.browser: self.browser.close(); self.browser=None
        finally:
            if self.playwright: self.playwright.stop(); self.playwright=None
