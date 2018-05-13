
#Native libraries
import os
import atexit
import pickle
#Installed libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#Constant Settings
DRIVER_PATH = "chromedriver" #Path to chromedriver bin
WINDOW_X = 1280 #Browser window size
WINDOW_Y = 720
TIMEOUT = 30 #Page Load Timeout
USERAGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"

class Webdriver(object):
    def __init__(self,
        driver_path=DRIVER_PATH,
        winsize=(WINDOW_X, WINDOW_Y),
        cookies_path=None,
        autosave_cookies=True,
        user_agent=USERAGENT,
        timeout=TIMEOUT,
        headless=True
    ):
        """Initialize a Chrome Webdriver object using Selenium.
        :param cookies_path: Path of cookies file (default=None=do not use cookies)
        :param autosave_cookies: Autosave cookies at exit? (default=True)
        :param headless: Execute headless browser? (default=True)
        The following params are default to Constant Settings on the .py file:
        :param driver_path: Path of chromedriver executable
        :param winsize: Browser window size, format: tuple/list (sizeX, sizeY)
        :param user_agent: User agent string for the browser
        :param timeout: Page load timeout
        """
        #Create options
        opts = Options()
        if headless:
            opts.add_argument("--headless")
        #opts.add_argument("--window-size={},{}".format(winsize[0], winsize[1]))
        opts.add_argument("user-agent="+user_agent)
        #Start browser
        self.browser = webdriver.Chrome(
            executable_path=driver_path,
            chrome_options=opts
        )
        self.browser.set_window_size(winsize[0], winsize[1])
        self.browser.set_page_load_timeout(timeout)
        #Some class attributes
        self.keys = Keys
        self.cookies_path = cookies_path
        self.autosave_cookies = autosave_cookies
        self.headless = headless
        self.window_size = winsize
        #Load cookies
        try:
            self.load_cookies()
        except FileNotFoundError: #If cookies file does not exist
            self.save_cookies() #create it
        #Atexit register (save cookies & stop browser when program ends)
        @atexit.register
        def atexit_f():
            self.stop()

    def get_browser(self):
        """Get the browser object
        :return: Selenium Webdriver chromedriver object
        """
        return self.browser

    def stop(self, save_cookies=None):
        """Stop the webdriver. For starting again, another Webdriver object must be initialized
        :param save_cookies: Auto-save cookies before closing the browser?
        If nothing is specified, value declared at autosave_cookies will be used
        """
        if save_cookies is None:
            save_cookies = self.autosave_cookies
        if save_cookies:
            self.save_cookies()
        self.browser.quit()

    def is_running(self):
        """Get current running status of webdriver
        :return: True if webdriver is running; False if is stopped
        """
        try:
            u = self.browser.current_url
        except:
            return False
        else:
            return True

    def screenshot(self, file_path=None):
        """Generate a PNG screenshot from the current window.
        The image will be saved or returned as bytes
        :param file_path: path to file where screenshot will be saved
        :return: image as bytes object if no path is provided
        """
        #TODO save full page screenshots
        sbytes = self.browser.get_screenshot_as_png()
        if file_path:
            with open(file_path, "wb") as file:
                file.write(sbytes)
        else:
            return sbytes

    def save_cookies(self):
        """Save the current cookies to a Pickle file
        on the cookies_path provided when initializing the Webdriver.
        """
        if self.cookies_path:
            cookies = self.browser.get_cookies()
            with open(self.cookies_path, "wb") as file:
                pickle.dump(cookies, file)

    def load_cookies(self):
        """Load the cookies saved on the Pickle file
        on the cookies_path provided when initializing the Webdriver.
        """
        if self.cookies_path:
            with open(self.cookies_path, "rb") as file:
                cookies = pickle.load(file)
                for c in cookies:
                    try:
                        self.browser.add_cookie(c)
                    except:
                        pass
