import logging
from playwright.sync_api import Page, expect
from pages.report_page import ReportPage


class SSPIUpdateWarningsInformationPage(ReportPage):

    # Selectable Options

    HEADER = "SSPI Update Warnings - Information"
    AGE_OPTIONS=["All", "Under 80", "80 and over"]
    REASONI_OPTIONS=["Removal", "Subject joined BSO", "Subject left BSO"]
    WARNINGI_OPTIONS=["Adoption", "Armed Services", "Embarkation", "Mental Hospital", "No open episodes", "No open or changed episodes", "Not provided", "Other reason", "Previous end code changed", "Removal", "Service dependent"]
    TABLE_ID="#sspiUpdateWarningList"
    TABLE_FIRST_ROW=f"{TABLE_ID} > tbody > tr:nth-child(1)"
    TABLE_FIRST_NHS_NUMBER=f"{TABLE_FIRST_ROW} > td:nth-child(3)"
    TABLE_FIRST_FAMILY_NAME=f"{TABLE_FIRST_ROW} > td:nth-child(4)"
    TABLE_FIRST_FIRST_NAME=f"{TABLE_FIRST_ROW} > td:nth-child(5)"
    API_REQUEST="**/bss/report/sspiUpdateWarnings/information/search**"

    def __init__(self, page: Page) -> None:
        ReportPage.__init__(self, page)
        self.page = page

    def verify_header(self) -> None:
        super().verify_header(self.HEADER)

    def set_done_drop_down(self, value: str) -> None:
        self.page.locator("#actionList").select_option(value)
        self.page.wait_for_timeout(5000)

    def enter_nhs_number(self, selected_nhs: str) -> None:
        self.page.locator("#nhsNumberFilter").get_by_role("textbox").fill(selected_nhs)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass

    def enter_family_name(self, selected_family_name: str) -> None:
        self.page.locator("#familyNameFilter").get_by_role("textbox").fill(selected_family_name)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass

    def enter_first_name(self, selected_first_name: str) -> None:
        self.page.locator("#firstGivenNameFilter").get_by_role("textbox").fill(selected_first_name)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass

    def sort_received(self) -> None:
        self.page.locator("#actionList").select_option("")
        self.page.get_by_label("Received: activate to sort").click()
        self.page.wait_for_timeout(5000)

    def table_filtered_by_age(self, selected_age: str) -> None:
        self.page.locator("#ageTodayList").select_option(selected_age)
        with self.page.expect_response("**/bss/report/sspiUpdateWarnings/information/search**") as response:
            pass

    def event_selected(self, selected_reason: str) -> None:
        self.page.locator("#eventList").select_option(selected_reason)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass

    def warning_selected(self, selected_warning: str) -> None:
        self.page.locator("#reasonList").select_option(selected_warning)
        with self.page.expect_response(self.API_REQUEST) as response:
            pass

    def sort_add_info(self) -> None:
        self.page.locator("#actionList").select_option("")
        self.page.get_by_label("Additional Info: activate to").click()
        self.page.wait_for_timeout(5000)
