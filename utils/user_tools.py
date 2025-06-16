import json
import os
import logging
from pathlib import Path
from playwright.sync_api import Page, expect
from pages.login.cognito_authentication import CognitoAuthenticationPage
from pages.login.org_selection import OrgSelectionPage

USERS_FILE = Path(__file__).parent.parent / "users.json"


class UserTools:
    """
    A utility class for retrieving and doing common actions with users.
    """

    def user_login(self, page: Page, user: str) -> None:
        """
        Logs into the BS-Select application and selects the applicable org (if required).

        Args:
            page (playwright.sync_api.Page): The Playwright page object to interact with.
            user (str): The user details required, in the format "Role Type" or "Role Type - Organisation".
        """
        page.goto("/bss")
        user = self.retrieve_user(user)

        if "cognito" in page.url:
            CognitoAuthenticationPage(page).cognito_login(
                user["username"], os.getenv("COGNITO_USER_PASSWORD")
            )
        else:
            page.locator("//input[@data-vv-as='User Name']").fill(user["uuid"])
            page.locator("//input[@data-vv-as='Password']").fill(
                os.getenv("USER_PASSWORD")
            )
            page.locator("//button[@class='nhsuk-button']").click()
        OrgSelectionPage(page).org_selection(user["role_to_select"])

    @staticmethod
    def retrieve_user(user: str) -> dict:
        """
        Retrieves the user information as a dict for the user provided.

        Args:
            user (str): The user details required, in the format "Role Type - Organisation".
        """
        with open(USERS_FILE, "r") as file:
            user_data = json.loads(file.read())

        if not user in user_data:
            raise Exception(f"User [{user}] is not present in users.json")

        return user_data[user]
