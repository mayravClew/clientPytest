from typing import Tuple
from selenium.webdriver.common.by import By
from models.client_model import Client
from pages.base_page import BasePage


class SingleClientPage(BasePage):
    """
    Page object model for the clients page of the application.

    This class provides the locators and methods for interacting with
    the single client page, including deleting a client.
    """

    def __init__(self, driver):
        """
        Initialize the SingleClientPage.

        :param driver: The WebDriver instance to use for interacting with the page.
        """
        super().__init__(driver)
        self.delete_button: Tuple[str, str] = (By.ID, "delete-client-id")
        self.delete_reason: Tuple[str, str] = (By.CSS_SELECTOR, "#userActionFeedback > div > div > form > "
                                                                "div.modal-body > div:nth-child(1) > div:nth-child(1)"
                                                                " > label")
        self.submit_reason_delete: Tuple[str, str] = (By.CSS_SELECTOR, 'div.modal-footer > div > button')

    def fin(self) ->None:
        """
        Delete the client.

        This method performs the steps to delete a client:
        1. Click the delete button.
        2. Select the reason for deletion.
        3. Submit the deletion form.
        """
        self.click(self.delete_button)
        self.click(self.delete_reason)
        self.click(self.submit_reason_delete)
