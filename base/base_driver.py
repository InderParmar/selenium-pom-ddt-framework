import time
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.config import EXPLICIT_WAIT

logger = logging.getLogger(__name__)


class BaseDriver:
    """
    Base class providing shared WebDriver utility methods.
    All page classes inherit from this.
    """

    def __init__(self, driver):
        self.driver = driver

    # ── Scrolling ────────────────────────────────────────────────────────────

    def page_scroll(self):
        """
        Scrolls to the bottom of the page incrementally until
        no new content is loaded.
        """
        logger.info("Starting full page scroll")
        page_height = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); "
            "return document.body.scrollHeight;"
        )

        while True:
            last_height = page_height
            time.sleep(2)
            page_height = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight); "
                "return document.body.scrollHeight;"
            )
            if last_height == page_height:
                logger.info("Reached end of page — scroll complete")
                break

    # ── Explicit Waits ───────────────────────────────────────────────────────

    def wait_for_presence_of_all_elements(self, locator_type, locator):
        """
        Waits until ALL elements matching the locator are present in the DOM.

        :param locator_type: By.XPATH, By.CSS_SELECTOR, etc.
        :param locator:      Locator string
        :return:             List of WebElements
        """
        logger.debug("Waiting for all elements | locator: %s", locator)
        wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        elements = wait.until(
            EC.presence_of_all_elements_located((locator_type, locator))
        )
        logger.debug("Found %d element(s) for locator: %s", len(elements), locator)
        return elements

    def wait_until_element_is_clickable(self, locator_type, locator):
        """
        Waits until a single element is visible AND clickable.

        :param locator_type: By.XPATH, By.CSS_SELECTOR, etc.
        :param locator:      Locator string
        :return:             WebElement
        """
        logger.debug("Waiting for clickable element | locator: %s", locator)
        wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        element = wait.until(
            EC.element_to_be_clickable((locator_type, locator))
        )
        logger.debug("Element is clickable: %s", locator)
        return element