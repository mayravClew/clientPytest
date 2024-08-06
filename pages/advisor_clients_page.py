from typing import Tuple, List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from models.client_model import Client
from pages.base_page import BasePage
from pages.single_client_page import SingleClientPage


class AdvisorClientsPage(BasePage):
    """
    Page object model for the advisor clients page of the application.

    This class provides the locators and methods for interacting with
    the clients page, including verifying client data and deleting clients.
    """

    def __init__(self, driver):
        """
        Initialize the AdvisorClientsPage.

        :param driver: The WebDriver instance to use for interacting with the page.
        """
        super().__init__(driver)
        self.user_name_field: Tuple[str, str] = (By.ID, "loginEmail")
        self.password_field: Tuple[str, str] = (By.ID, 'loginPassword')
        self.login_button: Tuple[str, str] = (By.XPATH, '//button[@type="{}"]'.format('submit'))
        self.firm_field: Tuple[str, str] = (By.ID, 'orgId')
        self.firm_options: Tuple[str, str] = (By.CSS_SELECTOR, '#orgId option')
        self.clients_table: Tuple[str, str] = (By.CSS_SELECTOR, '.my-clients-table tbody')
        self.single_client_page = SingleClientPage(driver)

    def add_client_button(self) -> None:
        """
        Click the button to add a new client.
        """
        self.click(self.new_client_button)

    def _get_all_rows(self) -> List[WebElement]:
        """
        Get all rows from the clients table.

        :return: A list of web elements representing the rows in the clients table.
        """
        table = self.driver.find_element(*self.clients_table)
        return table.find_elements(By.TAG_NAME, "tr")

    def verify_client_exists_at_grid(self, client_id: str) -> bool:
        """
        Verify that a client with the given ID exists in the clients table.

        :param client_id: The ID of the client to verify.
        :type client_id: str
        :return: True if the client exists in the table, False otherwise.
        :rtype: bool
        """
        return self.get_row(client_id) is not None

    def verify_client_data_at_grid(self, client_id: str, client: Client) -> bool:
        """
        Verify that the client data matches the expected values in the clients table.

        :param client_id: The ID of the client to verify.
        :type client_id: str
        :param client: The Client object containing the expected client data.
        :type client: Client
        :return: True if the client data matches, False otherwise.
        :rtype: bool
        """
        row = self.get_row(client_id)
        if row:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text == client_id:
                if (cells[1].text == client.first_name + ' ' + client.last_name and
                        cells[2].text == client.email and
                        cells[6].text == client.repId):
                    return True
        return False

    def get_row(self, client_id: str):
        """
        Get the row in the clients table corresponding to the given client ID.

        :param client_id: The ID of the client whose row is to be retrieved.
        :type client_id: str
        :return: The web element representing the row for the client, or None if not found.
        :rtype: Optional[WebElement]
        """
        rows = self._get_all_rows()
        row = next(
            (single_row for single_row in rows if single_row.find_elements(By.TAG_NAME, "td")[0].text == client_id),
            None)
        assert row, f'Row should not be null for client_id {client_id}'
        return row

    def fin(self, client_id: str) -> None:
        """
        Delete a client by clicking on their row and then confirming the deletion.

        :param client_id: The ID of the client to be deleted.
        :type client_id: str
        """
        self.get_row(client_id).click()
        self.single_client_page.fin()
