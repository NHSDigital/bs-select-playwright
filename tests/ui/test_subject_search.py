from pages.main_menu import MainMenuPage
from playwright.sync_api import Page
from utils.screenshot_tool import ScreenshotTool
from utils.user_tools import UserTools
from datetime import datetime


def login_as_bso_user(page: Page) -> None:
    UserTools().user_login(page, "BSO User - BS1")
    MainMenuPage(page).select_menu_option("Subject Search")


def test_search_by_nhs_number(page: Page) -> None:
    """
   This test verifies that searching for a specific NHS Number in the subject search returns exactly one unique result corresponding to the eligible subject.
    It ensures the search functionality correctly identifies and displays the subject based on their NHS Number
   """
    # Logged into BSS_SO1
    login_as_bso_user(page)

    eligible_subject_nhs_number = "900 001 9144"
    # Search by NHS Number
    page.fill("#nhsNumberFilter > input", eligible_subject_nhs_number)

    # Assert NHS Number appears in results
    page.wait_for_selector("//tbody/tr/td[2]")
    search_value = page.locator("//tbody/tr/td[2]").text_content()
    ScreenshotTool(page).take_screenshot("search_by_nhs_number")
    # asserting the eligible_subject_nhs_number and search_value
    assert eligible_subject_nhs_number == search_value
    # Assert only 1 result is returned
    assert page.locator("tbody > tr").count() == 1


def test_search_by_first_name(page: Page) -> None:
    """
    This test verifies that searching for a specific first_given_name in the subject search returns exactly one unique result corresponding to the eligible subject.
    It ensures the search functionality correctly identifies and displays the subject based on their first_given_name
    """
    # Logged into BSS_SO1
    login_as_bso_user(page)

    eligible_subject_first_name = "Kierra"
    # Search by first_given_name
    page.fill("#givenNameFilter > input", eligible_subject_first_name)

    # Assert first_name appears in results
    page.wait_for_selector("//tbody/tr/td[4]")
    search_value = page.locator("//tbody/tr/td[4]").text_content()
    ScreenshotTool(page).take_screenshot("search_by_first_given_name")

    # asserting the eligible_subject_first_name and search_value
    assert eligible_subject_first_name == search_value
    # Assert only 1 result is returned
    assert page.locator("tbody > tr").count() == 1


def test_search_by_family_name(page: Page) -> None:
    """
    This test verifies that searching for a specific family_name in the subject search returns exactly one unique result corresponding to the eligible subject.
    It ensures the search functionality correctly identifies and displays the subject based on their family_name
    """
    # Logged into BSS_SO1
    login_as_bso_user(page)

    eligible_subject_family_name = "BETA"
    # Search by family_name
    page.fill("#familyNameFilter > input", eligible_subject_family_name)

    # Assert family_name appears in results
    page.wait_for_selector("//tbody/tr/td[3]")
    search_value = page.locator("//tbody/tr/td[3]").text_content()
    ScreenshotTool(page).take_screenshot("search_by_family_name")

    # asserting the eligible_subject_family_name and search_value
    assert eligible_subject_family_name == search_value
    # Assert only 1 result is returned
    assert page.locator("tbody > tr").count() == 1


def test_search_by_date_of_birth(page: Page) -> None:
    """
    This test verifies that searching for a specific DOB in the subject search returns exactly one unique result corresponding to the eligible subject.
    It ensures the search functionality correctly identifies and displays the subject based on their DOB
    """
    # Logged into BSS_SO1
    login_as_bso_user(page)

    eligible_subject_dob = "01-Jun-1987"
    # Search by family_name
    page.fill("#bornFilter > input", eligible_subject_dob)
    page.click("body")

    # Assert dob appears in results
    page.wait_for_selector("//tbody/tr/td[5]")
    search_value = page.locator("//tbody/tr/td[5]").text_content()
    ScreenshotTool(page).take_screenshot("search_by_dob")

    # asserting the eligible_subject_family_name and search_value
    assert eligible_subject_dob == search_value
    # Assert only 1 result is returned
    assert page.locator("tbody > tr").count() == 1

##TODO: Implement search by date_of_death
def test_search_by_date_of_death(page: Page) -> None:
    """
    This test verifies that searching for a specific date_of_death in the subject search returns exactly one unique result corresponding to the eligible subject.
    It ensures the search functionality correctly identifies and displays the subject based on their date_of_death
    """
    # Logged into BSS_SO1
    login_as_bso_user(page)

    eligible_subject_nhs_number = ""
    current_date = datetime.now().strftime("%d-%b-%Y")
    print(current_date)


def test_too_many_subjects_message(page: Page) -> None:
    """
    Subject search returning more than 50 subjects shows a message to further filter down the search criteria
    """
    login_as_bso_user(page)

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
    login_as_bso_user(page)

    eligible_subject_outcode = "A99"
    page.fill("#outcodeFilter > input", eligible_subject_outcode)
    page.wait_for_selector("//tbody/tr/td[contains(., 'A99')]")
    search_value = page.locator("//tbody/tr/td[contains(., 'A99')]").text_content()

    # asserting the eligible_subject_outcode and search_value
    assert eligible_subject_outcode == search_value
    # Assert only 1 result is returned
    assert page.locator("tbody > tr").count() == 1
    ScreenshotTool(page).take_screenshot("search_by_outcode")

def test_click_row_navigates_to_subject_details(page: Page) -> None:
    """
    When a user clicks on a row in the results table they are taken to the subject details page for that subject
    """
    login_as_bso_user(page)

    eligible_subject_nhs_number = "900 001 9144"
    page.fill("#nhsNumberFilter > input", eligible_subject_nhs_number)
    page.wait_for_selector("//tbody/tr/td[2]")
    # Click the row
    page.dblclick("//tbody/tr[1]")

    page.wait_for_selector("text=Subject Details")
    assert page.is_visible("text=Subject Details")
    ScreenshotTool(page).take_screenshot("navigates_to_subject_page")
