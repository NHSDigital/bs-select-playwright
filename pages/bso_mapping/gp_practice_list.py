import logging
from playwright.sync_api import Page, expect
from pages.report_page import ReportPage


class GPListPage(ReportPage):
    HEADER = "GP Practice List"

    def __init__(self, page: Page) -> None:
        ReportPage.__init__(self, page)
        self.page = page
