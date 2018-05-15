
#Native libraries
#import os
import atexit
#Installed libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#Constant Settings
DRIVER_PATH = "chromedriver" #Path to chromedriver bin
DATA_PATH = "ChromeDriverData" #Path to store browser data (history, cookies...)
WINDOW_X = 1280 #Browser window size
WINDOW_Y = 720
TIMEOUT = 30 #Page Load Timeout
USERAGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"

class Webdriver(object):
    def __init__(self,
        headless=True,
        driver_path=DRIVER_PATH,
        data_path=DATA_PATH,
        winsize=(WINDOW_X, WINDOW_Y),
        user_agent=USERAGENT,
        timeout=TIMEOUT
    ):
        """Initialize a Chrome Webdriver object using Selenium.
        :param headless: Execute headless browser? (default=True)
        The following params are default to Constant Settings on the .py file:
        :param driver_path: Path of chromedriver executable
        :param data_path: Path for browser data
        :param winsize: Browser window size, format: tuple/list (sizeX, sizeY)
        :param user_agent: User agent string for the browser
        :param timeout: Page load timeout
        """
        #Create options
        opts = Options()
        if headless:
            opts.add_argument("--headless")
        #opts.add_argument("--window-size={},{}".format(winsize[0], winsize[1]))
        opts.add_argument("user-data-dir="+data_path)
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
        self.headless = headless
        self.window_size = winsize
        self.data_path = data_path
        self.user_agent = user_agent
        #Atexit register (stop browser when program ends)
        @atexit.register
        def atexit_f():
            self.stop()

    def get_browser(self):
        """Get the browser object
        :return: Selenium Webdriver chromedriver object
        """
        return self.browser

    def stop(self):
        """Stop the webdriver.
        For starting again, another Webdriver object must be initialized
        """
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

    def get_windows(self):
        """Get all the windows/tabs currently opened on the browser
        :return: List of windows/tabs names
        """
        return self.browser.window_handles

    def switch_window(self, window=None, index=None):
        """Switch to a window/tab of the browser.
        Specify the window with:
        :param window: Window name to switch to
        :param index: Index of the window to switch to
        """
        w = None
        if window is not None and index is None:
            w = window
        if window is None and index is not None:
            w = self.get_windows()[index]
        if w is not None:
            self.browser.switch_to_window(w)

    def close_window(self, window=None, index=None, switch=True):
        """Close an opened window/tab of the browser.
        Specify the window with:
        :param window: Window name to switch to
        :param index: Index of the window to switch to
        Additional params:
        :param switch: Index of the window to switch to after the operation
        if switch=True (default), browser will switch to last available window
        """
        w = None
        if window is not None and index is None:
            w = window
        if window is None and index is not None:
            w = self.get_windows()[index]
        if w is not None:
            self.browser.switch_to_window(w)
            self.browser.close()
            if switch is True:
                w = self.get_windows()[-1]
            else:
                w = self.get_windows()[switch]
            self.switch_window(window=w)

    def close_windows(self, startIndex, lastIndex=None):
        """Close all opened windows/tabs on the browser between two indexes given (zero-indexed, both inclusive).
        I.e. if we want to close all tabs except except the first one, startIndex=1.
        After the operation, browser will switch to the last window available.
        :param startIndex: index of first tab (required)
        :param lastIndex: index of last tab (optional)
        If lastIndex not provided, all tabs from startIndex will be closed
        """
        windows = self.get_windows()
        if lastIndex is None:
            lastIndex = len(windows) - 1
        for i in range(startIndex, lastIndex+1):
            try:
                win = windows[i]
                self.switch_window(window=win)
                self.browser.close()
            except:
                pass
        self.switch_window(index=-1)

