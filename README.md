# Webdriver Manager

A Python class to help using a headless chromedriver Webdriver with Selenium on Python.

Requirements:

* Python 3.x (tested on 3.4, 3.5, 3.6)
* Selenium for Python (available via pip)
* chromedriver binary (remember to set it as executable)
* Google Chrome or Chromium installed on the system (required by chromedriver)

## Functions and examples

_TODO: Add examples for switching between opened windows/tabs_

### Basic initialization

```python
from webdrivermgr import Webdriver
driver = Webdriver()
browser = driver.get_browser()
browser.get("https://www.google.com")
```

### Set webdriver bin location, data folder and custom proxy
```python
from webdrivermgr import Webdriver
driver = Webdriver(
    driver_path="/home/me/.webdrivers/chromedriver",
    data_path="/home/me/.chromedriverdata",
    proxy="127.0.0.1:9999"
)
browser = driver.get_browser()
browser.get("https://www.google.com")
```

### Get a PNG screenshot

```python
from webdrivermgr import Webdriver
driver = Webdriver()
browser = driver.get_browser()
browser.get("https://www.google.com")
#We can save the screenshot to a file
driver.screenshot("/home/david/my_screenshot.png")
#or get the bytes object from the image
photo = driver.screenshot()
```

### Closing

```python
from webdrivermgr import Webdriver
driver = Webdriver(
    cookies_path="/home/david/mycookies.pkl"
)
browser = driver.get_browser()
browser.get("https://www.google.com")
#The browser automatically stops when the main application ends, using atexit
#Or we can stop it anytime with:
driver.stop()
#After stopping the webdriver, another Webdriver object must be initialized
#if we want to run the webdriver again!
```
