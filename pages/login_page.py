from typing import Tuple
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page object model for the login page of the application.

    This class provides the locators and methods for interacting with
    the login page, including performing the login action.
    """

    def __init__(self, driver):
        """
        Initialize the LoginPage.

        :param driver: The WebDriver instance to use for interacting with the page.
        """
        super().__init__(driver)
        self.user_name_field: Tuple[str, str] = (By.ID, "loginEmail")
        self.password_field: Tuple[str, str] = (By.ID, 'loginPassword')
        self.login_button: Tuple[str, str] = (By.XPATH, '//button[@type="{}"]'.format('submit'))
        self.firm_field: Tuple[str, str] = (By.ID, 'orgId')
        self.firm_options: Tuple[str, str] = (By.CSS_SELECTOR, '#orgId option')

    def login(self) -> None:
        """
        Perform the login action by filling in the username and password,
        selecting the firm, and clicking the login button.
        """
        try:
            # Navigate to the login page
            self.driver.get('https://advisor-test.pontera.com/business/auth/signin.html')
            self.wait_for(self.user_name_field)
            print("Page has finished loading")
        except Exception as e:
            print(f"Error while loading page: {e}")

        # Fill in the username and password
        self.fill_text(self.user_name_field, 'Maayan+Tester1@feex.com')
        self.fill_text(self.password_field, 'Advisor0103Buckley')

        # Click the login button
        self.click(self.login_button)

        # Wait for the firm field to be visible and select the firm
        self.wait_for(self.firm_field)
        self.click(self.firm_field)
        self.select_option(self.firm_options, 'QA Advisors')

        # Click the login button again
        self.click(self.login_button)
        self.wait_for(self.new_client_button)
