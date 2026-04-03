import time
import logging
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.utils import Utils

logger = logging.getLogger(__name__)


class SearchFlightResultsPage(BaseDriver):
    """
    Page Object for the flight search results page on Yatra.
    Handles stop-filter interactions and results retrieval.
    """

    # ── Locators ─────────────────────────────────────────────────────────────
    _FILTER_1_STOP  = "//p[@class='font-lightgrey bold'][normalize-space()='1']"
    _FILTER_2_STOPS = "//p[@class='font-lightgrey bold'][normalize-space()='2']"
    _FILTER_0_STOPS = "//p[@class='font-lightgrey bold'][normalize-space()='0']"
    _ALL_STOPS_LIST = "//div[@class='pl-10 stop-cont']//span[contains(@aria-label,'Stop')]"

    # Accepted stop filter values
    STOP_OPTIONS = {"0 Stop", "1 Stop", "2 Stops"}

    def __init__(self, driver):
        super().__init__(driver)

    # ── Element Accessors ────────────────────────────────────────────────────

    def _get_filter_1_stop(self):
        return self.wait_until_element_is_clickable(By.XPATH, self._FILTER_1_STOP)

    def _get_filter_2_stops(self):
        return self.wait_until_element_is_clickable(By.XPATH, self._FILTER_2_STOPS)

    def _get_filter_0_stops(self):
        return self.wait_until_element_is_clickable(By.XPATH, self._FILTER_0_STOPS)

    # ── Actions ──────────────────────────────────────────────────────────────

    def filter_flights_by_stops(self, stops: str):
        """
        Applies the stop-count filter on the search results page.

        :param stops: One of '0 Stop', '1 Stop', or '2 Stops'
        :raises ValueError: If an unsupported stop value is supplied
        """
        logger.info("Applying flight filter: '%s'", stops)
        time.sleep(4)   # allow results panel to settle

        filter_map = {
            "0 Stop": self._get_filter_0_stops,
            "1 Stop": self._get_filter_1_stop,
            "2 Stops": self._get_filter_2_stops,
        }

        if stops not in filter_map:
            logger.error(
                "Invalid stop filter '%s'. Accepted values: %s",
                stops, self.STOP_OPTIONS,
            )
            raise ValueError(f"Invalid stop filter: '{stops}'. Use one of {self.STOP_OPTIONS}.")

        filter_map[stops]().click()
        logger.info("Filter '%s' applied successfully", stops)
        time.sleep(4)   # allow results to reload after filter

    def get_all_stop_elements(self) -> list:
        """
        Returns all stop-indicator elements currently visible in the results.

        :return: List of WebElements each containing a stop label (e.g. '1 Stop')
        """
        logger.info("Fetching all stop indicator elements from results")
        elements = self.wait_for_presence_of_all_elements(By.XPATH, self._ALL_STOPS_LIST)
        logger.info("Total result rows found: %d", len(elements))
        return elements