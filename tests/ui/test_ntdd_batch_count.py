import datetime
import re
import pytest
from playwright.sync_api import Page, expect
from pages.main_menu import MainMenuPage
from utils.screenshot_tool import ScreenshotTool
from utils.table_utils import TableUtils
from utils.user_tools import UserTools
from datetime import datetime, timedelta


def test_ntdd_end_date_warning_for_past_date(page: Page):
    # Navigate to the NTDD batch creation page
    UserTools().login_and_navigate(page, "BSO User - BS1", "Batch Management", "Create NTDD Batch")

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
    UserTools().login_and_navigate(page, "BSO User - BS1", "Batch Management", "Create NTDD Batch")

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

    MainMenuPage(page).select_menu_option("Batch Management", "Batch List")
    expect(page.locator("h1.bss-page-title")).to_have_text("Batch List")

    page.locator("th#batchIdFilter > input").fill(batch_id)
    # Wait for the table to update — ensure only 1 row is visible
    expect(page.locator("#batchList tbody tr")).to_have_count(1)

    table = TableUtils(page, "#batchList")
    row_count = table.get_row_count()
    assert row_count == 1, f"Expected 1 row, found {row_count}"

    row_data = table.get_row_data_with_headers(0)
    ScreenshotTool(page).take_screenshot("test_count_ntdd_batch")

    assert row_data["BSO Batch ID"] == batch_id, \
        f"Expected batch_id '{batch_id}', got '{row_data['BSO Batch ID']}'"

    assert row_data["Batch Type"] == "NTDD", \
        f"Expected batch_type '{"NTDD"}', got '{row_data['Batch Type']}'"

    assert row_data["Batch Title"] == batch_title, \
        f"Expected batch_title '{batch_title}', got '{row_data['Batch Title']}'"

    today = datetime.today().strftime("%d-%b-%Y")  # e.g., "01-Aug-2025"
    assert row_data["Count Date"] == today, \
        f"Expected Count Date '{today}', got '{row_data['Count Date']}'"

    assert int(row_data["Count"]) > 0, \
        f"Expected Count to be greater than 0, got '{row_data['Count']}'"

    # Double-click on the filtered row
    page.locator("#batchList tbody tr").first.dblclick()

    # Delete the batch
    page.locator("#deleteButton").click()
    page.locator("#confirmButtonInDeletePopup").click()
    # Confirm batch is deleted
    expect(page.locator(f"text={batch_title}")).not_to_be_visible()


def enter_date_for_selection(page: Page, days_offset: int) -> None:
    target_date = (datetime.today() + timedelta(days=days_offset)).strftime("%d-%b-%Y")
    page.locator("#ntdEndDate").fill(target_date)
