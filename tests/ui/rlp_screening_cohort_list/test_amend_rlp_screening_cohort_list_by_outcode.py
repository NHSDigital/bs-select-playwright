import pytest
from pages.rlp_cohort_list_page import CohortListPage
from playwright.sync_api import expect, Page, Playwright
from datetime import datetime
from pages.rlp_location_list_page import ScreeningLocationListPage
from utils.test_helpers import generate_random_string
from utils.user_tools import UserTools, login_and_navigate


# creating cohort for below test
def test_create_screening_cohort_outcode_test_data(
    page: Page, rlp_cohort_list_page: CohortListPage
) -> None:
    """
    Test to create a test data
    """
    # Logged into BSS_SO2 user2
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Cohort List")

    # Test data
    cohort_name = "Hadley"
    attendance_rate = "25"
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    # creating cohort using create cohort method
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )


## Test_35
def test_outcode_try_amend_cohort_by_dbl_click_and_invoke_pencil_icon(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """
    Trying to amend cohort using the methods - double_clicking on the cohort and invoking the pencil icon
    """
    # Logged into BSS_SO2 user2
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Cohort List")

    # Test data
    cohort_name = f"cohort_name-{datetime.now()}"
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    attendance_rate = "25"
    # creating cohort using create cohort method
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )

    # Filter the newly created cohort and double_clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    expect(page.get_by_text("Amend Screening Cohort")).to_be_visible()
    # cancelling to amend
    rlp_cohort_list_page.click_amend_cohort_cancel_button()

    # Filter the newly created cohort and clicking on the cohort pencil to amend(testing pencil icon)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.click_filtered_cohort_pencil_icon()
    expect(page.get_by_text("Amend Screening Cohort")).to_be_visible()


## Test_36 positive data validation
@pytest.mark.parametrize("input_length", [3, 100])
def test_outcode_amend_cohort_name_with_valid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, input_length,
    check_and_create_unit_test_data, check_and_create_location_test_data_for_outcode
):
    """
    Creating a cohort using outcode to amend the name field using the min and max length
    """
    # Logged into BSS_SO2 user2
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Cohort List")

    # creating cohort
    cohort_name = f"cohort_name-{datetime.now()}"
    attendance_rate = 25
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )
    # Filter the newly created cohort and double_clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    # Amending the cohort name
    amend_cohort_name = generate_random_string(input_length)
    rlp_cohort_list_page.enter_amend_screening_cohort_name(amend_cohort_name)
    rlp_cohort_list_page.click_amend_save_btn()
    rlp_cohort_list_page.enter_screening_cohort_name_filter(amend_cohort_name)
    filtered_amend_name = rlp_cohort_list_page.value_of_filtered_cohort_name()
    assert amend_cohort_name == filtered_amend_name


## Test_36 negative field data validation
@pytest.mark.parametrize(
    "amend_name, expected_message",
    [
        ("$%&@", "Screening Cohort Name contains invalid characters"),
        ("cd", "The Screening Cohort Name you entered is too short"),
        ("     ", "Screening Cohort Name must be populated"),
        ("Hadley", "Screening Cohort Name is already in use by another cohort"),
    ],
)
def test_outcode_amend_screening_cohort_with_invalid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, amend_name, expected_message
):
    """Test to verify error messages for outcode amend cohort with invalid data "$%&@", " "-empty string, Name is already in use, too short"""
    # Logged into BSS_SO2 user2
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Cohort List")

    # creating cohort
    cohort_name = f"cohort_name-{datetime.now()}"
    attendance_rate = 25
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )
    # Filter the newly created cohort and double_clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    # Amending cohort name field
    rlp_cohort_list_page.enter_amend_screening_cohort_name(amend_name)
    rlp_cohort_list_page.click_amend_save_btn()
    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


## Test_37 positive field data validation for amend Expected Attendance Rate
@pytest.mark.parametrize("input_value", ["0.0", "100.0"])
def test_outcode_amend_expected_attendance_rate_valid_data(
    page: Page, rlp_cohort_list_page: CohortListPage, input_value
) -> None:
    """outcode amend expected attendance rate valid data"""
    # Logged into BSS_SO2 user2
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Cohort List")

    # creating cohort
    cohort_name = f"cohort_name-{datetime.now()}"
    attendance_rate = 25
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )
    # Filter the newly created cohort and double-clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    # Amend attendance rate
    rlp_cohort_list_page.enter_amend_expected_attendance_rate(input_value)
    rlp_cohort_list_page.click_amend_save_btn()

    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    filtered_amend_attendance = rlp_cohort_list_page.value_of_filtered_attendance()
    assert input_value == filtered_amend_attendance


#### Test_37 negative test for amend Expected Attendance Rate field
@pytest.mark.parametrize(
    "amend_attendance_rate, expected_message",
    [
        ("cd", "Invalid value"),
        ("     ", "Expected Attendance Rate must be between 0 and 100"),
    ],
)
def test_outcode_amend_expected_attendance_rate_invalid_data(
    page: Page,
    rlp_cohort_list_page: CohortListPage,
    amend_attendance_rate,
    expected_message,
):
    """Test to verify error messages for outcode amend cohort with invalid data "$%&@", " "-empty string, Name is already in use, too short"""
    # Logged into BSS_SO2 user2
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Cohort List")

    # creating cohort
    cohort_name = f"cohort_name-{datetime.now()}"
    attendance_rate = 25
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )
    # Filter the newly created cohort and double-clicking on the cohort to amend(testing double click)
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    # Amend attendance rate
    rlp_cohort_list_page.enter_amend_expected_attendance_rate(amend_attendance_rate)
    rlp_cohort_list_page.click_amend_save_btn()
    # Assert that the correct error message is displayed based on invalid_data
    expect(page.get_by_text(expected_message)).to_be_visible()


#### Test_40
def test_outcode_amend_included_outcodes_are_visible(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """created a cohort, amened the cohort by including the outcodes"""
    # Logged into BSS_SO1
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Cohort List")

    # creating cohort
    cohort_name = f"cohort_name-{datetime.now()}"
    attendance_rate = 25
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    out_code1 = "EX1"
    out_code2 = "EX2"
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.click_select_outcodes_btn()
    rlp_cohort_list_page.enter_outcode_filter(out_code1)
    rlp_cohort_list_page.click_add_btn_to_select_outcode(out_code1)
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert included_outcodes == 1
    rlp_cohort_list_page.click_select_outcodes_btn()
    rlp_cohort_list_page.enter_outcode_filter(out_code2)
    rlp_cohort_list_page.click_add_btn_to_select_outcode(out_code2)
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert included_outcodes == 2


## Test_41
def test_outcode_amend_remove_added_outcodes(
    page: Page, rlp_cohort_list_page: CohortListPage
):
    """
    created a cohort, amened the cohort by including the outcodes, and removed the outcodes
    """
    # Logged into BSS_SO1
    login_and_navigate(page, "Read Only BSO User - BS2", "Round Planning", "Screening Cohort List")

    # creating cohort
    cohort_name = f"cohort_name-{datetime.now()}"
    attendance_rate = 25
    location_name = "Poundland Car Park - Alberta Retail Park"
    unit_name = "Batman"
    out_code1 = "EX1"
    out_code2 = "EX2"
    out_code3 = "EX3"
    rlp_cohort_list_page.create_cohort_outcode_without_gp(
        cohort_name, str(attendance_rate), location_name, unit_name
    )
    rlp_cohort_list_page.enter_screening_cohort_name_filter(cohort_name)
    rlp_cohort_list_page.dbl_click_on_filtered_cohort()
    page.wait_for_timeout(3000)
    rlp_cohort_list_page.click_select_outcodes_btn()
    rlp_cohort_list_page.enter_outcode_filter(out_code1)
    rlp_cohort_list_page.click_add_btn_to_select_outcode(out_code1)
    rlp_cohort_list_page.enter_outcode_filter(out_code2)
    rlp_cohort_list_page.click_add_btn_to_select_outcode(out_code2)
    rlp_cohort_list_page.enter_outcode_filter(out_code3)
    rlp_cohort_list_page.click_add_btn_to_select_outcode(out_code3)
    rlp_cohort_list_page.click_done_btn_gp_practices_include_popup()
    included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert included_outcodes == 3

    # removing one included gp practice
    rlp_cohort_list_page.click_remove_button_by_gp_code("EX1")
    removed_included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_outcodes == 2
    # removing one included gp practice
    rlp_cohort_list_page.click_remove_button_by_gp_code("EX2")
    removed_included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_outcodes == 1
    # removing last of the included gp practice
    rlp_cohort_list_page.click_remove_button_by_gp_code("EX3")
    removed_included_outcodes = page.locator(
        "//table[@id='practicesToIncludeList']//tr//td[2]"
    ).count()
    assert removed_included_outcodes == 0
