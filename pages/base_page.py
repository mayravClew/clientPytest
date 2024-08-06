from typing import Tuple, Union
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains, Chrome, Edge, Firefox, Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

class BasePage:
    """
    Base class for all page objects, providing common methods and utilities
    for interacting with web elements.

    :param driver: The WebDriver instance to use for interacting with the page.
    """

    def __init__(self, driver: Union[Chrome, Firefox, Edge]):
        """
        Initialize the BasePage.

        :param driver: The WebDriver instance to use for interacting with the page.
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.new_client_button: Tuple[str, str] = (By.CSS_SELECTOR, '#addNewClientBtnId')

    def click(self, locator: Tuple[str, str]) -> None:
        """
        Click on a web element identified by the locator.

        :param locator: A tuple containing the By strategy and the locator of the element.
        """
        el: WebElement = self.wait.until(
            expected_conditions.element_to_be_clickable(locator)
        )
        el.click()

    def fill_text(self, locator: Tuple[str, str], txt: str) -> None:
        """
        Fill text into a web element identified by the locator.

        :param locator: A tuple containing the By strategy and the locator of the element.
        :param txt: The text to be filled into the element.
        """
        el: WebElement = self.wait.until(
            expected_conditions.element_to_be_clickable(locator)
        )
        el.click()
        el.clear()
        el.send_keys(txt)

    def wait_for(self, locator: Tuple[str, str]) -> WebElement:
        """
        Wait for a web element to be clickable and return it.

        :param locator: A tuple containing the By strategy and the locator of the element.
        :return: The web element that is clickable.
        """
        el: WebElement = self.wait.until(
            expected_conditions.element_to_be_clickable(locator)
        )
        return el

    def select_option(self, locator: Tuple[str, str], txt: str) -> None:
        """
        Select an option from a dropdown or list identified by the locator.

        :param locator: A tuple containing the By strategy and the locator of the options list.
        :param txt: The text of the option to be selected.
        """
        self.wait.until(
            expected_conditions.presence_of_element_located(locator)
        )
        option_list = self.driver.find_elements(By.CSS_SELECTOR, locator[1])
        requested = next((x for x in option_list if txt in x.text), None)
        assert requested, f'Option {txt} was not visible'
        requested.click()

    def clear_text(self, locator: Tuple[str, str]) -> None:
        """
        Clear the text from a web element identified by the locator.

        :param locator: A tuple containing the By strategy and the locator of the element.
        """
        el: WebElement = self.wait.until(
            expected_conditions.element_to_be_clickable(locator)
        )
        el.clear()

    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get the text of a web element identified by the locator.

        :param locator: A tuple containing the By strategy and the locator of the element.
        :return: The text of the web element.
        """
        el: WebElement = self.wait.until(
            expected_conditions.visibility_of_element_located(locator)
        )
        return el.text

    def move_to_element(self, webelement: WebElement) -> None:
        """
        Move the mouse to a web element.

        :param webelement: The web element to move the mouse to.
        """
        action = ActionChains(self.driver)
        self.wait.until(expected_conditions.visibility_of(webelement))
        action.move_to_element(webelement).perform()

    def is_elem_displayed(self, locator: Tuple[str, str]) -> bool:
        """
        Check if a web element identified by the locator is displayed.

        :param locator: A tuple containing the By strategy and the locator of the element.
        :return: True if the element is displayed, False otherwise.
        """
        try:
            self.wait.until(
                expected_conditions.element_to_be_clickable(locator)
            )
            return True
        except StaleElementReferenceException:
            return False
        except NoSuchElementException:
            return False

    def go_back(self) -> None:
        """
        Navigate back in the browser history.
        """
        self.driver.execute_script("window.history.go(-2)")
