import time
import logging
import pytest
from ddt import ddt, data, unpack

from pages.yatra_launch_page import YatraLaunchPage
from utilities.utils import Utils
from config.config import JSON_FILE

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("setup")
@ddt
class TestFlightStopFilter(Utils):
    """
    Validates that applying a stop-count filter on Yatra.com
    correctly restricts all displayed results to that stop count.

    Test Data: testdata/testdata.json
    Keys     : going_from, going_to, depart_date, return_date, stops
    """

    @pytest.fixture(autouse=True)
    def initialise_pages(self, setup):
        """Initialises page objects before each test."""
        self.launch_page = YatraLaunchPage(self.driver)
        self.ut = Utils()   # ← separate Utils instance, tracks soft asserts correctly

    @data(*Utils.read_data_from_json(JSON_FILE))
    @unpack
    def test_flight_stop_filter(
        self,
        going_from: str,
        going_to: str,
        depart_date: str,
        return_date: str,
        stops: str,
    ):
        """
        Test Steps:
          1. Search for flights between two cities on given dates.
          2. Apply the stop-count filter (0 / 1 / 2 Stop).
          3. Scroll to load all paginated results.
          4. Assert every result card shows the expected stop count.
        """
        logger.info(
            "─── TEST START | %s → %s | Dates: %s – %s | Filter: %s ───",
            going_from, going_to, depart_date, return_date, stops,
        )

        # Step 1 — Search
        results_page = self.launch_page.search_flights(
            going_from, going_to, depart_date, return_date
        )

        # Step 2 — Apply filter
        results_page.filter_flights_by_stops(stops)

        # Step 3 — Scroll to load all results
        self.launch_page.page_scroll()

        # Step 4 — Fetch all stop elements
        all_stop_elements = results_page.get_all_stop_elements()
        logger.info(
            "Verifying %d result(s) against filter '%s'",
            len(all_stop_elements), stops,
        )

        # Step 5 — Soft assert on self.ut so failures are tracked on its instance
        self.ut.assert_list_item_text(all_stop_elements, stops)

        logger.info(
            "─── TEST END | %s → %s | Filter: %s ───",
            going_from, going_to, stops,
        )
        time.sleep(20)