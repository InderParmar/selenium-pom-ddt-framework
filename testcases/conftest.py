import os
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config.config import BASE_URL, PAGE_LOAD_WAIT

logger = logging.getLogger(__name__)

# ── Cross-icon that appears on Yatra homepage ─────────────────────────────────
_POPUP_CROSS = "span[class='style_cross__q1ZoV'] img[alt='cross']"


# ── Browser fixture ───────────────────────────────────────────────────────────

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome",
        help="Browser to run tests on: chrome | safari"
    )


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="function")
def setup(request, browser):
    """
    Sets up and tears down the WebDriver for each test function.
    Attaches the driver to the test class so pages can access it.
    """
    browser = browser.lower()
    logger.info("Initialising browser: %s", browser)

    if browser == "chrome":
        chrome_options = Options()
        # chrome_options.add_argument("--headless")   # uncomment for CI
        driver = webdriver.Chrome(options=chrome_options)
    elif browser == "safari":
        driver = webdriver.Safari()
    else:
        pytest.fail(f"Unsupported browser: '{browser}'. Use 'chrome' or 'safari'.")

    driver.maximize_window()
    wait = WebDriverWait(driver, PAGE_LOAD_WAIT)

    logger.info("Navigating to: %s", BASE_URL)
    driver.get(BASE_URL)

    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, _POPUP_CROSS))).click()
        logger.info("Welcome popup dismissed")
    except Exception:
        logger.warning("Popup cross not found or already dismissed — continuing")

    request.cls.driver = driver
    yield
    logger.info("Test complete — quitting browser")
    driver.quit()


# ── HTML Report Hooks ─────────────────────────────────────────────────────────

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Captures a screenshot on test failure and embeds it in the HTML report.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        test_failed = report.failed and not xfail
        test_skipped_xfail = report.skipped and xfail

        if test_failed or test_skipped_xfail:
            report_dir = os.path.dirname(item.config.option.htmlpath)
            # sanitise node id for use as a filename
            safe_name = report.nodeid.replace("::", "_").replace("/", "_")
            screenshot_name = f"{safe_name}.png"
            screenshot_path = os.path.join(report_dir, screenshot_name)

            try:
                item.cls.driver.save_screenshot(screenshot_path)
                logger.info("Screenshot saved: %s", screenshot_path)
                html_img = (
                    f'<div><img src="{screenshot_name}" alt="Failure screenshot" '
                    f'style="width:320px;height:200px;border:1px solid #ccc;" '
                    f'onclick="window.open(this.src)" align="right"/></div>'
                )
                extra.append(pytest_html.extras.html(html_img))
            except Exception as e:
                logger.error("Could not save screenshot: %s", e)

        report.extra = extra


def pytest_html_report_title(report):
    report.title = "✈  Yatra Flight Filter — Automation Test Report"