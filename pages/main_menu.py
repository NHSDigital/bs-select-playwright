import logging
from playwright.sync_api import Page
from pages.base_page import BasePage


class MainMenuPage(BasePage):
    HEADER = "Welcome to Breast Screening Select"

    def __init__(self, page: Page) -> None:
        BasePage.__init__(self, page)
