import logging
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


PAGE_HEADER = "Choose Organisation"


class OrgSelectionPage(BasePage):

    def __init__(self, page: Page) -> None:
        BasePage.__init__(self, page)
        self.page = page

    def org_selection(self, role: str = None) -> None:
        expect(self.page.get_by_text("Breast Screening Select")).to_be_visible()
        if self.page.url.endswith("/bss/orgChoice"):
            self.verify_header()
            if role is not None:
                logging.info(f"Selecting role: {role}")
                org_selector = self.page.locator("#chosenOrgCode")
                options = org_selector.locator("option")
                option_count = options.count()
                found = False
                for i in range(option_count):
                    text = options.nth(i).get_attribute("value")
                    if role == text:
                        found = True
                        org_selector.select_option(role)
                        break

                if not found:
                    raise AssertionError(f"Login failed: '{role}' not found on /orgChoice screen.")
                org_selector.select_option(role)
                self.page.get_by_role("button", name="Select Organisation").click()

    def verify_header(self) -> None:
        return super().verify_header(PAGE_HEADER)
