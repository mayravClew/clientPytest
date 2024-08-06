import time

import pytest
import allure
from models import client_model
from pages.advisor_clients_page import AdvisorClientsPage
from pages.login_page import LoginPage
from pages.new_client_page import NewClientPage
from selenium_interface import SeleniumInterface


@pytest.fixture(scope="module")
def selenium_interface():
    """
    Fixture to initialize Selenium interface.
    This fixture sets up the Selenium driver and quits it after the tests are done.
    """
    interface = SeleniumInterface()
    yield interface
    interface.driver.quit()


@pytest.fixture(scope="module")
def clients_page(selenium_interface):
    """
    Fixture to initialize the Advisor Clients Page.
    """
    clients = AdvisorClientsPage(selenium_interface.driver)
    return clients


@pytest.fixture(scope="module")
def new_clients_page(selenium_interface):
    """
    Fixture to initialize the New Client Page.
    """
    return NewClientPage(selenium_interface.driver)


@pytest.fixture(scope="module")
def login(selenium_interface):
    """
    Fixture to log in to the application.
    """
    login_page = LoginPage(selenium_interface.driver)
    login_page.login()


@allure.feature('Client Management')
@allure.story('Add Client')
@pytest.mark.usefixtures("login")
def test_add_client(clients_page, new_clients_page):
    """
    Test to add a new client and verify the client's data in the grid.
    """
    with allure.step("Add a new client"):
        # Define client data
        client_data = client_model.Client(
            first_name='first', last_name='last', ssn_tin='123581220',
            email="client@yahoo.com", contactPhone='1235812200',
            city='mycity', state='Alaska', repId='Maayan Tester1'
        )

        # Add new client
        clients_page.add_client_button()
        client_id = new_clients_page.add_client(client_data)

    with allure.step("Verify the new client exists in clients' grid"):
        time.sleep(2)
        client_data.clientId = client_id
        assert client_id, 'The ID of the created client should not be None'
        assert clients_page.verify_client_exists_at_grid(client_id), 'Client should exist in the grid'
        ret_val = clients_page.verify_client_data_at_grid(client_id, client_data)

    with allure.step("Verify new client details in clients' grid"):
        assert ret_val, f"Client's data in the grid did not match the expected client data: {client_data}"
        clients_page.fin(client_id)


if __name__ == "__main__":
    pytest.main()
