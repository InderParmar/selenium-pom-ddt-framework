import time
import logging
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from pages.search_flights_results_page import SearchFlightResultsPage

logger = logging.getLogger(__name__)


class YatraLaunchPage(BaseDriver):
    """
    Page Object for the Yatra.com homepage.
    Handles flight search form interactions.
    """

    # ── Locators ─────────────────────────────────────────────────────────────
    _DEPART_FROM_CLICK  = "//p[@title='New Delhi']"
    _DEPART_FROM_INPUT  = "//input[@class='MuiInputBase-input MuiInput-input css-mnn31']"
    _GOING_TO_CLICK     = "//p[@title='Mumbai']"
    _GOING_TO_INPUT     = "//input[@id='input-with-icon-adornment']"
    _DEPART_RESULTS     = "//div[@class='MuiBox-root css-0']//child::li[@class='test css-1izsdd5']"
    _GOING_TO_RESULTS   = '//div[@class="MuiBox-root css-134xwrj"]//li[@class="test css-1izsdd5"]'
    _ORIGIN_DATE_FIELD  = "//div[@class='css-13lub7m']"
    _RETURN_DATE_FIELD  = "div.css-d6c8u4"
    _SEARCH_BUTTON      = (
        "//button[@class='MuiButtonBase-root MuiButton-root MuiButton-button "
        "MuiButton-buttonPrimary MuiButton-sizeMedium MuiButton-buttonSizeMedium "
        "MuiButton-colorPrimary MuiButton-root MuiButton-button MuiButton-buttonPrimary "
        "MuiButton-sizeMedium MuiButton-buttonSizeMedium MuiButton-colorPrimary  css-18xeq64']"
    )

    def __init__(self, driver):
        super().__init__(driver)

    # ── Element Accessors ────────────────────────────────────────────────────

    def _depart_from_trigger(self):
        return self.wait_until_element_is_clickable(By.XPATH, self._DEPART_FROM_CLICK)

    def _depart_from_input(self):
        return self.driver.find_element(By.XPATH, self._DEPART_FROM_INPUT)

    def _going_to_trigger(self):
        return self.driver.find_element(By.XPATH, self._GOING_TO_CLICK)

    def _going_to_input(self):
        return self.driver.find_element(By.XPATH, self._GOING_TO_INPUT)

    def _origin_date_field(self):
        return self.driver.find_element(By.XPATH, self._ORIGIN_DATE_FIELD)

    def _return_date_field(self):
        return self.driver.find_element(By.CSS_SELECTOR, self._RETURN_DATE_FIELD)

    def _search_button(self):
        return self.wait_until_element_is_clickable(By.XPATH, self._SEARCH_BUTTON)

    def _depart_dropdown_results(self):
        return self.wait_for_presence_of_all_elements(By.XPATH, self._DEPART_RESULTS)

    def _going_to_dropdown_results(self):
        return self.wait_for_presence_of_all_elements(By.XPATH, self._GOING_TO_RESULTS)

    # ── Helper: Dropdown Selection ───────────────────────────────────────────

    def _select_from_dropdown(self, results: list, keyword: str):
        """
        Iterates dropdown suggestions and clicks the first match.

        :param results: List of suggestion WebElements
        :param keyword: Text to match against each suggestion
        """
        logger.debug("Scanning %d suggestion(s) for keyword '%s'", len(results), keyword)
        for item in results:
            if keyword in item.text:
                logger.debug("Match found: '%s' — clicking", item.text.strip())
                item.click()
                return
        logger.warning("No dropdown match found for keyword '%s'", keyword)

    # ── Actions ──────────────────────────────────────────────────────────────

    def enter_depart_from(self, location: str):
        """Clicks the Depart-From field and types the departure city."""
        logger.info("Entering departure location: '%s'", location)
        time.sleep(4)
        self._depart_from_trigger().click()
        self._depart_from_input().send_keys(location)
        logger.debug("Keys sent for departure location")
        time.sleep(4)
        self._select_from_dropdown(self._going_to_dropdown_results(), location)

    def enter_going_to(self, location: str):
        """Clicks the Going-To field and types the destination city."""
        logger.info("Entering destination location: '%s'", location)
        time.sleep(4)
        self._going_to_trigger().click()
        self._going_to_input().send_keys(location)
        logger.debug("Keys sent for destination location")
        time.sleep(4)
        self._select_from_dropdown(self._depart_dropdown_results(), location)

    def select_dates(self, departure_date: str, return_date: str):
        """
        Selects departure and return dates from the calendar widget.

        :param departure_date: e.g. 'April 3rd'
        :param return_date:    e.g. 'April 8th'
        """
        logger.info("Selecting dates — Departure: '%s' | Return: '%s'",
                    departure_date, return_date)
        self._origin_date_field().click()
        time.sleep(4)
        self.driver.find_element(
            By.CSS_SELECTOR, f'div[aria-label*="{departure_date}"]'
        ).click()
        logger.debug("Departure date '%s' selected", departure_date)
        time.sleep(4)

        self._return_date_field().click()
        time.sleep(4)
        self.driver.find_element(
            By.CSS_SELECTOR, f'div[aria-label*="{return_date}"]'
        ).click()
        logger.debug("Return date '%s' selected", return_date)
        time.sleep(4)

    def click_search(self):
        """Clicks the Search Flights button."""
        logger.info("Clicking Search button to submit flight query")
        self._search_button().click()

    def search_flights(
        self,
        depart_location: str,
        going_to_location: str,
        departure_date: str,
        return_date: str,
    ) -> SearchFlightResultsPage:
        """
        End-to-end flight search: fills every field and submits the form.

        :return: SearchFlightResultsPage instance for chaining
        """
        logger.info(
            "Starting flight search | %s → %s | %s to %s",
            depart_location, going_to_location, departure_date, return_date,
        )
        self.enter_depart_from(depart_location)
        self.enter_going_to(going_to_location)
        self.select_dates(departure_date, return_date)
        self.click_search()
        logger.info("Search submitted — navigating to results page")
        return SearchFlightResultsPage(self.driver)