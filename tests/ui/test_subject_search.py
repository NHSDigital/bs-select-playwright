import pytest

from pages.main_menu import MainMenuPage
from playwright.sync_api import Page
from utils.screenshot_tool import ScreenshotTool
from utils.table_utils import TableUtils
from utils.user_tools import UserTools
from datetime import datetime


@pytest.fixture(scope="function", autouse=True)
def login_as_bso_user(page: Page) -> None:
    """
    Automatically logs in as BSO User - BS1 before every test.
    """
    UserTools().user_login(page, "BSO User - BS1")
    MainMenuPage(page).select_menu_option("Subject Search")


def test_search_by_first_name(page: Page) -> None:
    """
    This test verifies that searching for a specific first_given_name in the subject search returns exactly one unique result corresponding to the eligible subject.
    It ensures the search functionality correctly identifies and displays the subject based on their first_given_name
    """
    eligible_subject_first_name = "Kierra"

    # Search by first_given_name
    page.fill("#givenNameFilter > input", eligible_subject_first_name)
    page.wait_for_selector("#subjectList tbody > tr")

    table = TableUtils(page, "#subjectList")
    row_count = table.get_row_count()
    assert row_count == 1, f"Expected 1 row, found {row_count}"

    row_data = table.get_row_data_with_headers(0)
    ScreenshotTool(page).take_screenshot("search_by_first_name")

    assert row_data["First Given Name"] == eligible_subject_first_name, \
        f"Expected first name '{eligible_subject_first_name}', got '{row_data['First Given Name']}'"


def test_search_by_family_name(page: Page) -> None:
    """
    This test verifies that searching for a specific family_name in the subject search returns exactly one unique result corresponding to the eligible subject.
    It ensures the search functionality correctly identifies and displays the subject based on their family_name
    """
    eligible_subject_family_name = "BETA"
    page.fill("#familyNameFilter > input", eligible_subject_family_name)
    page.wait_for_selector("#subjectList tbody > tr")

    table = TableUtils(page, "#subjectList")
    row_count = table.get_row_count()
    assert row_count == 1, f"Expected 1 row, found {row_count}"

    row_data = table.get_row_data_with_headers(0)
    ScreenshotTool(page).take_screenshot("search_by_family_name")

    assert row_data["Family Name"] == eligible_subject_family_name, \
        f"Expected family name '{eligible_subject_family_name}', got '{row_data['Family Name']}'"


def test_search_by_date_of_birth(page: Page) -> None:
    """
    This test verifies that searching for a specific DOB in the subject search returns exactly one unique result corresponding to the eligible subject.
    It ensures the search functionality correctly identifies and displays the subject based on their DOB
    """
    eligible_subject_dob = "01-Jun-1987"

    # Search by born field
    page.fill("#bornFilter > input", eligible_subject_dob)
    page.click("body")
    page.wait_for_selector("#subjectList tbody > tr")

    table = TableUtils(page, "#subjectList")
    row_count = table.get_row_count()
    assert row_count == 1, f"Expected 1 row, found {row_count}"

    row_data = table.get_row_data_with_headers(0)
    ScreenshotTool(page).take_screenshot("search_by_date_of_birth")

    assert row_data["Born"] == eligible_subject_dob, \
        f"Expected DOB '{eligible_subject_dob}', got '{row_data['Born']}'"


def test_search_by_date_of_death(page: Page) -> None:
    """
    This test verifies that searching for a specific date_of_death in the subject search returns exactly one unique result corresponding to the eligible subject.
    It ensures the search functionality correctly identifies and displays the subject based on their date_of_death
    """

    eligible_subject_date_of_death = "05-May-2017"
    # Search by died field
    page.fill("#diedFilter > input", eligible_subject_date_of_death)
    page.click("body")
    page.wait_for_selector("#subjectList tbody > tr")

    table = TableUtils(page, "#subjectList")
    row_count = table.get_row_count()
    assert row_count == 1, f"Expected 1 row, found {row_count}"

    row_data = table.get_row_data_with_headers(0)
    ScreenshotTool(page).take_screenshot("search_by_date_of_death")

    assert row_data["Died"] == eligible_subject_date_of_death, \
        f"Expected date of death '{eligible_subject_date_of_death}', got '{row_data['Died']}'"


def test_too_many_subjects_message(page: Page) -> None:
    """
    Subject search returning more than 50 subjects shows a message to further filter down the search criteria
    """

    eligible_subject_first_name = "maria"
    # Search by first_given_name
    page.fill("#givenNameFilter > input", eligible_subject_first_name)
    # Clear search fields
    page.fill("#nhsNumberFilter > input", "")
    page.fill("#bsoFilter > input", "")

    # Assert message is displayed
    page.wait_for_selector("text=Your request contained more than 50 results. Please enter more search criteria to narrow the results")
    ScreenshotTool(page).take_screenshot("too_many_subjects_message")


def test_search_by_outcode(page: Page) -> None:
    """
    User searches for a subject by outcode
    """

    eligible_subject_outcode = "A99"
    page.fill("#outcodeFilter > input", eligible_subject_outcode)
    page.wait_for_selector("#subjectList tbody > tr")

    table = TableUtils(page, "#subjectList")
    row_count = table.get_row_count()
    # Assert that only one row is returned for the given outcode
    assert row_count == 1, f"Expected 1 row, found {row_count}"

    # Retrieve data from the first (and only) row as a dictionary of column headers to cell values
    row_data = table.get_row_data_with_headers(0)
    ScreenshotTool(page).take_screenshot("search_by_outcode")

    # Assert that the "Outcode" column in the row matches the expected outcode
    assert row_data["Outcode"] == eligible_subject_outcode, \
        f"Expected outcode '{eligible_subject_outcode}', got '{row_data['Outcode']}'"


def test_search_and_navigate_to_subject_details(page: Page) -> None:
    """
    Verifies that searching by NHS Number returns the correct subject,
    and clicking the row navigates to the Subject Details page.
    """
    eligible_subject_nhs_number = "900 001 9144"

    # Search by NHS Number
    page.fill("#nhsNumberFilter > input", eligible_subject_nhs_number)
    page.wait_for_selector("#subjectList tbody > tr")

    table = TableUtils(page, "#subjectList")

    # Get the number of visible rows in the filtered table
    row_count = table.get_row_count()
    assert row_count == 1, f"Expected 1 row, found {row_count}"

    # Retrieve the row data
    row_data = table.get_row_data_with_headers(0)

    # Assert that the NHS Number column matches the expected value
    assert row_data["NHS Number"].strip() == eligible_subject_nhs_number, \
        f"Expected NHS Number '{eligible_subject_nhs_number}', got '{row_data['NHS Number'].strip()}'"

    ScreenshotTool(page).take_screenshot("search_result")

    # Double-click the row to navigate to Subject Details
    table.pick_row(0).dblclick()
    page.wait_for_selector("text=Subject Details")

    # Confirm that the Subject Details page is visible
    assert page.is_visible("text=Subject Details"), "Subject Details page not displayed"

    ScreenshotTool(page).take_screenshot("navigates_to_subject_page")


# Column config for below sort test
SORT_COLUMN_CONFIG = {
    "family_name": {
        "header_selector": "#columnHeaderFamilyName",
        "column_index": 3,
        "value_type": str,
        "screenshot": "sorted_by_family_name",
        "filter_selector": "#givenNameFilter > input",
        "filter_value": "Hilary"
    },
    "given_name": {
        "header_selector": "#columnHeaderGivenName",
        "column_index": 4,
        "value_type": str,
        "screenshot": "sorted_by_first_given_name",
        "filter_selector": "#familyNameFilter > input",
        "filter_value": "BOYD"
    },
    "date_of_birth": {
        "header_selector": "#columnHeaderBorn",
        "column_index": 5,
        "value_type": "date",
        "screenshot": "sorted_by_date_of_birth",
        "filter_selector": "#givenNameFilter > input",
        "filter_value": "Hilary"
    },
    "outcode": {
        "header_selector": "#columnHeaderOutcode",
        "column_index": 6,
        "value_type": str,
        "screenshot": "sorted_by_outcode",
        "filter_selector": "#givenNameFilter > input",
        "filter_value": "Hilary"
    },
    "nhs_number": {
        "header_selector": "#columnHeaderNhsNumber",
        "column_index": 2,
        "value_type": int,
        "screenshot": "sorted_by_nhs_number",
        "filter_selector": "#givenNameFilter > input",
        "filter_value": "Hilary"
    }
}


@pytest.mark.parametrize("column_name", SORT_COLUMN_CONFIG.keys())
def test_subject_list_sorting(page, column_name):
    """
    Reusable test to verify sorting on various columns in the subject list.
    """
    config = SORT_COLUMN_CONFIG[column_name]

    # Apply filter to ensure table is populated
    page.fill(config["filter_selector"], config["filter_value"])
    page.wait_for_selector("#subjectList tbody > tr")

    ensure_sorted_column(
        page,
        config["header_selector"],
        config["column_index"],
        config["value_type"],
        config["screenshot"]
    )


def ensure_sorted_column(page, header_selector, column_index, value_type, screenshot_name):
    def get_values():
        cells = page.locator(f"//tbody/tr/td[{column_index}]").all_text_contents()
        if value_type == int:
            return [int(val.replace(" ", "")) for val in cells]
        elif value_type == "date":
            return [datetime.strptime(val.strip(), "%d-%b-%Y") for val in cells]
        return [val.strip() for val in cells]

    # Initial click
    page.click(header_selector)
    page.wait_for_timeout(1000)
    values = get_values()

    if values != sorted(values):
        # Try again in case the table was sorted in descending order by default
        page.click(header_selector)
        page.wait_for_timeout(1000)
        values = get_values()

    ScreenshotTool(page).take_screenshot(screenshot_name)

    # Final assertion
    assert values == sorted(values), f"Values in column {column_index} not sorted: {values}"



