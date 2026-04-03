import os

# ── Base Paths ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TESTDATA_DIR  = os.path.join(BASE_DIR, "testdata")
REPORTS_DIR   = os.path.join(BASE_DIR, "reports")
LOGS_DIR      = os.path.join(BASE_DIR, "logs")

# ── Test Data Files ──────────────────────────────────────────
JSON_FILE  = os.path.join(TESTDATA_DIR, "testdata.json")
EXCEL_FILE = os.path.join(TESTDATA_DIR, "test_data.xlsx")

# ── Application ──────────────────────────────────────────────
BASE_URL       = "https://www.yatra.com/"
BROWSER        = "chrome"

# ── Timeouts (seconds) ───────────────────────────────────────
IMPLICIT_WAIT  = 10
EXPLICIT_WAIT  = 40
PAGE_LOAD_WAIT = 30

# ── Ensure runtime directories exist ────────────────────────
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR,    exist_ok=True)