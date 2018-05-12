# Webdriver Manager

A Python class to help using a headless chromedriver Webdriver with Selenium.

## Functions and examples

### Initialize

```python
    from webdrivermgr import Webdriver
    driver = Webdriver()
    browser = driver.get_browser()
    browser.get("https://www.google.com")
```

### Use cookies

```python
    from webdrivermgr import Webdriver
    driver = Webdriver(cookies_path="/home/david/mycookies.pkl")
    browser = driver.get_browser()
    browser.get("https://www.google.com")
    #Cookies are loaded automatically when driver starts
    driver.load_cookies()
    #Cookies are saved automatically when driver stops
    driver.save_cookies()
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
    #If webdriver is using cookies, they'll be saved automatically
    driver.stop()
    #But we can avoid auto-cookies saving
    driver.stop(save_cookies=False)
    #We also can avoid auto-cookies saving when webdriver ends
    driver = Webdriver(
        cookies_path="/home/david/mycookies.pkl",
        autosave_cookies=False
    )
    #After stopping the webdriver, another Webdriver object must be initialized
    #if we want to run the webdriver again
```
