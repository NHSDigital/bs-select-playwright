import datetime
import re
import pytest
from playwright.sync_api import Page, expect
from pages.main_menu import MainMenuPage
from utils.screenshot_tool import ScreenshotTool
from utils.user_tools import UserTools
from datetime import datetime, timedelta


def login_and_navigate(page: Page, user: str, main_menu: str, sub_menu: str) -> None:
    """Helper function to log in and navigate to the desired menu."""
    UserTools().user_login(page, user)
    MainMenuPage(page).select_menu_option(main_menu, sub_menu)


def test_ntdd_end_date_warning_for_past_date(page: Page):
    # Navigate to the NTDD batch creation page
    login_and_navigate(page, "BSO User - BS1", "Batch Management", "Create NTDD Batch")

    # Fill in BSO Batch ID and Title
    page.fill("#bsoBatchId", "LAV979245E")
    page.fill("input#title", "Playwright_Test")

    # Set NTD End Date to yesterday
    enter_date_for_selection(page, -1)
    # Fill Start Age: 50 years 1 month
    page.fill("#startAgeYears", "50")
    page.fill("#startAgeMonths", "1")

    # Fill End Age: 70 years 11 months
    page.fill("#endAgeYears", "70")
    page.fill("#endAgeMonths", "11")

    # Click the "Count" button
    page.click("#countButtonText")

    # Wait until the warning message is visible
    warning = page.locator("#ntddBatchWarnings")
    warning.wait_for(state="visible")

    # Assert the warning popup is displayed with the correct message
    expect(warning).to_be_visible()
    expect(warning).to_contain_text("NTD End Date is in the past.")
    ScreenshotTool(page).take_screenshot("ntdd_end_date_warning_for_past_date")

    # click "Cancel" to close the warning popup
    page.click("#cancelButtonInWarningsPopup")


def test_count_ntdd_batch(page: Page) -> None:
    # Navigate to the NTDD batch creation page
    login_and_navigate(page, "BSO User - BS1", "Batch Management", "Create NTDD Batch")

    # Prepare batch with standard parameters
    batch_id = "LAV979245E"
    batch_title = "Happy Days Batch"
    page.fill("#bsoBatchId", batch_id)
    page.fill("input#title", batch_title)
    enter_date_for_selection(page, 5)
    # Fill Start Age: 50 years 1 month
    page.fill("#startAgeYears", "50")
    page.fill("#startAgeMonths", "1")
    # Fill End Age: 70 years 11 months
    page.fill("#endAgeYears", "70")
    page.fill("#endAgeMonths", "11")

    # Click the "Count" button
    page.click("#countButtonText")

    # Wait for the page to load and assert the header
    expect(page.locator("h1")).to_have_text("Amend NTDD Batch")
    # Assert Batch Title is correctly displayed
    expect(page.locator("#title")).to_have_value(batch_title)
    # Assert BSO BatchID is correctly recorded
    expect(page.locator("#bsoBatchId")).to_have_text(batch_id)

    # Assert NTD End Date is in correct format
    actual_date = page.locator("#ntdEndDate")
    # Get the value from the input field
    date_value = actual_date.input_value()
    assert datetime.strptime(date_value, "%d-%b-%Y")
    # Assert subject count is correctly recorded
    count_locator = page.locator(".col-md-2.data-field.control-label.number")
    # Assert the locator is visible
    expect(count_locator).to_be_visible()
    # Get the inner text and extract the numeric part
    subject_count_text = count_locator.text_content().strip()
    # Use regex to get the first number
    match = re.search(r"\d+", subject_count_text)
    assert match, f"Could not find a valid number in: '{subject_count_text}'"
    # Convert to int and assert value > 0
    count_value = int(match.group())
    assert count_value > 0, f"Expected count to be > 0, but got {count_value}"

    # Delete the batch
    page.locator("#deleteButton").click()
    page.locator("#confirmButtonInDeletePopup").click()
    # Confirm batch is deleted
    expect(page.locator(f"text={batch_title}")).not_to_be_visible()


def enter_date_for_selection(page: Page, days_offset: int) -> None:
    target_date = (datetime.today() + timedelta(days=days_offset)).strftime("%d-%b-%Y")
    page.locator("#ntdEndDate").fill(target_date)
