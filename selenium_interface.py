from selenium import webdriver


class SeleniumInterface:
    def __init__(self):
        self.driver = None
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--start-maximized")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=options)

    # Close the driver
    def _quit(self):
        self.driver.quit()
