from django.test import LiveServerTestCase
from utils.browser import make_chrome_browser
import time

class HomePageFuncTest(LiveServerTestCase):
    def sleep(self, seconds=5):
        time.sleep(seconds)
    

    def test_the_test(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        self.sleep(6)
        
        browser.quit()