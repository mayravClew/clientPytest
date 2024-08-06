import time
from typing import Tuple
from selenium.webdriver.common.by import By
from models.client_model import Client
from pages.base_page import BasePage


class NewClientPage(BasePage):
    """
    Page object model for the new client page of the application.

    This class provides the locators and methods for interacting with
    the new client page, including adding a new client.
    """

    def __init__(self, driver):
        """
        Initialize the NewClientPage.

        :param driver: The WebDriver instance to use for interacting with the page.
        """
        super().__init__(driver)
        self.first_name: Tuple[str, str] = (By.ID, "first_name")
        self.last_name: Tuple[str, str] = (By.ID, "last_name")
        self.ssn_tin: Tuple[str, str] = (By.ID, "ssn")
        self.email: Tuple[str, str] = (By.ID, "email")
        self.contactPhone: Tuple[str, str] = (By.ID, "contactPhone")
        self.city: Tuple[str, str] = (By.ID, "city")
        self.state: Tuple[str, str] = (By.XPATH, '//button[@title="{}"]'.format('Select state'))
        self.state_options: Tuple[str, str] = (By.CSS_SELECTOR, 'ul li')
        self.repId: Tuple[str, str] = (By.XPATH, '//button[@title="{}"]'.format('Select Advisor'))
        self.repId_options: Tuple[str, str] = (By.CSS_SELECTOR, 'ul li')
        self.add_client_button: Tuple[str, str] = (By.ID, 'save-client-changes-btn')
        self.client_id_label: Tuple[str, str] = (By.CSS_SELECTOR, '.field-name')
        self.client_id_value: Tuple[str, str] = (By.XPATH, '//*[@id ="client-identification"]/div[1]/div[1]/span[2]')

    def add_client(self, client: Client) -> str:
        """
        Add a new client using the provided client data.

        :param client: A Client object containing the client's details.
        :return: The client ID of the newly added client.
        """
        self.fill_text(self.first_name, client.first_name)
        self.fill_text(self.last_name, client.last_name)
        self.fill_text(self.ssn_tin, client.ssn_tin)
        self.fill_text(self.email, client.email)
        self.fill_text(self.contactPhone, client.contactPhone)
        self.fill_text(self.city, client.city)
        self.click(self.state)
        self.select_option(self.state_options, client.state)
        self.click(self.repId)
        self.wait_for(self.repId_options)
        time.sleep(3)
        self.select_option(self.repId_options, client.repId)
        self.click(self.add_client_button)

        # Wait for clients page to open
        self.wait_for(self.client_id_label)
        self.wait_for(self.client_id_value)

        # Retrieve and return the client ID
        client_id = self.get_text(self.client_id_value)

        # Go back to clients list page
        self.go_back()
        return client_id
