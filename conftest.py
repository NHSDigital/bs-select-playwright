"""
This is a conftest.py file for pytest, which is used to set up fixtures and hooks for testing.
This file is used to define fixtures that can be used across multiple test files.
It is also used to define hooks that can be used to modify the behavior of pytest.
"""

import logging
import os
from pathlib import Path
import typing
from collections.abc import MutableMapping
from typing import Any

import pytest
from dotenv import load_dotenv
from _pytest.python import Function
from pytest_html.report_data import ReportData
from playwright.sync_api import Page, sync_playwright

from pages.main_menu import MainMenuPage
from pages.ni_ri_sp_batch_page import NiRiSpBatchPage

from utils.db_util import DbUtil
from utils.db_restore import DbRestore
from utils.user_tools import UserTools, login_and_navigate

from pages.rlp_cohort_list_page import CohortListPage
from pages.rlp_location_list_page import ScreeningLocationListPage
from pages.rlp_unit_list_page import ScreeningUnitListPage
from utils.user_tools import UserTools

logger = logging.getLogger(__name__)
LOCAL_ENV_PATH = Path(os.getcwd()) / "local.env"


@pytest.fixture(autouse=True, scope="session")
def import_local_env_file() -> None:
    """
    This fixture is used to import the local.env file into the test environment (if the file is present),
    and will populate the environment variables prior to any tests running.
    If environment variables are set in a different way when running (e.g. via cli), this will
    prioritise those values over the local.env file.

    NOTE: You should not use this logic to read a .env file in a pipeline or workflow to set sensitive values.
    """
    if Path.is_file(LOCAL_ENV_PATH):
        load_dotenv(LOCAL_ENV_PATH, override=False)


@pytest.fixture(scope="session")
def user_tools() -> UserTools:
    return UserTools()


@pytest.fixture
def main_menu(page: Page) -> MainMenuPage:
    return MainMenuPage(page)


@pytest.fixture
def rlp_location_list_page(page: Page) -> ScreeningLocationListPage:
    return ScreeningLocationListPage(page)


@pytest.fixture
def rlp_cohort_list_page(page: Page) -> CohortListPage:
    return CohortListPage(page)


@pytest.fixture
def rlp_unit_list_page(page: Page) -> ScreeningUnitListPage:
    return ScreeningUnitListPage(page)


@pytest.fixture
def ni_ri_sp_batch_page(page: Page) -> NiRiSpBatchPage:
    return NiRiSpBatchPage(page)


## Fixture for ci-infra
@pytest.fixture
def db_util():
    db = DbUtil(host = os.getenv("CI_INFRA_DB_HOST"),
                port=os.getenv("CI_INFRA_DB_PORT"),
                dbname=os.getenv("CI_INFRA_DBNAME"),
                user=os.getenv("CI_INFRA_DB_USER"),
                password=os.getenv("CI_INFRA_DB_PASSWORD"))
    return db

# This variable is used for JSON reporting only
ENVIRONMENT_DATA = None


@pytest.fixture(autouse=True, scope="session")
def environment_info(metadata: object, base_url: str) -> None:
    APPLICATION_DETAILS = "Application Details"
    DATABASE_DETAILS = "Database Details"

    def filter_result(results: dict, key: str) -> str:
        """This is for tidying up the response for the HTML report"""
        string_to_return = ""
        for item in results[key]:
            if string_to_return != "":
                string_to_return += "<br />"
            string_to_return += f"{item}: {results[key][item]}"
        return string_to_return

    if base_url is not None:
        try:  # Try to get metadata first using a playwright object, but don't fail if it can't retrieve it
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(base_url=base_url)
                result = context.request.get(
                    "/bss/info",
                    headers={
                        "Host": f"{base_url}".replace("https://", "").replace("/", ""),
                        "Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br",
                    },
                    ignore_https_errors=True,
                )
                metadata[APPLICATION_DETAILS] = filter_result(
                    result.json(), APPLICATION_DETAILS
                )
                metadata[DATABASE_DETAILS] = filter_result(
                    result.json(), DATABASE_DETAILS
                )
                global ENVIRONMENT_DATA
                ENVIRONMENT_DATA = result.json()
                context.close()
                browser.close()

        except Exception as ex:
            logger.warning("Not been able to capture environment data for this run.")
            logger.warning(f"Exception: {ex}")
            metadata[APPLICATION_DETAILS] = "Unable to retrieve"
            metadata[DATABASE_DETAILS] = "Unable to retrieve"


# --- JSON Report Generation ---


@pytest.hookimpl(optionalhook=True)
def pytest_json_runtest_metadata(item: object) -> dict:
    formatted_description = str(item.function.__doc__).replace("\n", "")
    return {"description": " ".join(formatted_description.split())}


@pytest.hookimpl(optionalhook=True)
def pytest_json_modifyreport(json_report: MutableMapping[str, Any]) -> None:
    # Add env data to json report if present
    if ENVIRONMENT_DATA != None:
        json_report["environment_data"] = ENVIRONMENT_DATA


# --- HTML Report Generation ---


def pytest_html_report_title(report: ReportData) -> None:
    report.title = "BS-Select Test Automation Report"


def pytest_html_results_table_header(cells: list) -> None:
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report: object, cells: list) -> None:
    description = getattr(report, "description", "N/A")
    cells.insert(2, f"<td>{description}</td>")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Function) -> typing.Generator[None, None, None]:
    outcome = yield
    if outcome is not None:
        report = outcome.get_result()
        report.description = str(item.function.__doc__)


@pytest.fixture(scope="function", autouse=False)
def check_and_create_unit_test_data(
    page: Page, rlp_cohort_list_page: CohortListPage, context
):
    """Create unit test data for User2 BS2. Fixture to log in and ensure specific unit test data is created."""
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Unit List")
    unit_names = ["Batman", "Captain"]
    for unit_name in unit_names:
        rlp_cohort_list_page.create_unit_if_not_exists(unit_name)
    context.clear_cookies()

@pytest.fixture(scope="function", autouse=False)
def check_and_create_location_test_data_for_outcode(
    page: Page, rlp_cohort_list_page: CohortListPage, context
):
    """Generate location test data for User2 BS2. Fixture to log in and ensure specific location test data is created."""
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Location List")
    locations = [
        "Aldi - Caldecott County Retail Park",
        "Poundland Car Park - Alberta Retail Park",
    ]
    for location in locations:
        ScreeningLocationListPage(page).create_location_if_not_exists(location)
    context.clear_cookies()
