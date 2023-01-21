from selenium import webdriver


def set_web_driver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless=chrome')  # without opening browser window
    options.add_argument('no-sandbox')
    options.add_argument("user-agent=Chrome/80.0.3987.132")
    options.add_argument("--window-size=1920,1080")
    return options
