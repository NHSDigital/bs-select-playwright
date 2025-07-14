from playwright.sync_api import Page
from pages.monitoring_reports.sspi_update_warnings_base import SSPIUpdateWarningsBasePage


class SSPIUpdateWarningsActionPage(SSPIUpdateWarningsBasePage):
    # Selectable Options
    HEADER = "SSPI Update Warnings - Action"
    AGE_OPTIONS = ["All", "Under 80", "80 and over"]
    REASON_OPTIONS = [
        "Date of birth changed",
        "Date of death set",
        "Date of death cleared",
        "Gender changed",
        "NHS number changed",
        "NHS number superseded",
        "Subject joined BSO",
        "Subject left BSO",
    ]
    WARNING_OPTIONS = [
        "Age now inside programme",
        "Age now inside programme - Open episode",
        "Age now outside programme",
        "Age now outside programme - Open episode",
        "Date of death cleared",
        "Gender is Indeterminate",
        "Male with SC end code",
        "Male with no history",
        "Male with screening events",
        "No open episodes",
        "Open episode closed",
        "Subject has open episode",
        "Subject has HR status",
        "Subject has screening events",
        "Subject is ceased",
        "Under 44 with batch episodes",
        "Was below age limit now above",
        "Was below age limit now above - Open episode",
        "Was previously male",
    ]
    TABLE_ID = "#sspiUpdateWarningList"
    TABLE_FIRST_ROW = f"{TABLE_ID} > tbody > tr:nth-child(1)"
    TABLE_FIRST_NHS_NUMBER = f"{TABLE_FIRST_ROW} > td:nth-child(3)"
    TABLE_FIRST_FAMILY_NAME = f"{TABLE_FIRST_ROW} > td:nth-child(4)"
    TABLE_FIRST_FIRST_NAME = f"{TABLE_FIRST_ROW} > td:nth-child(5)"

    def __init__(self, page: Page) -> None:
        SSPIUpdateWarningsBasePage.__init__(self, page)
        self.API_REQUEST = "**/bss/report/sspiUpdateWarnings/action/search**"
