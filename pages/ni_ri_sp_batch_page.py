from __future__ import annotations
from datetime import datetime, timedelta
from playwright.sync_api import Page, expect
import logging
from utils.table_utils import TableUtils
from utils.screenshot_tool import ScreenshotTool


class NiRiSpBatchPage:

    def __init__(self, page: Page) -> None:

        self.page = page
        self.bso_batch_id_input = page.locator("#bsoBatchId")
        self.selection_date_input = page.locator("#rispSelectionDate")
        self.year_of_birth_from_input = page.locator("#earliestBirthYear")
        self.year_of_birth_to_input = page.locator("#latestBirthYear")
        self.month_of_birth_to_input = page.locator("#latestBirthMonth")
        self.count_button = page.locator("#countButtonText")
        self.page_heading = page.locator("h1.bss-page-title")
        self.include_specified_practices_radio_btn = page.locator(
            "#include_specified_practices"
        )
        self.include_specified_practice_groups_radio_btn = page.locator(
            "#include_specified_practice_groups"
        )
        self.include_specified_outcodes_radio_btn = page.locator(
            "#include_specified_outcodes"
        )
        self.include_specified_outcode_groups_radio_btn = page.locator(
            "#include_specified_outcode_groups"
        )
        self.excluded_gp_practices_filter = page.locator(
            "#gpPracticeSelection div.box1 input.filter"
        )
        self.gp_practices_select_move_single_arrow = page.locator(
            "#gpPracticeSelection div.box1 button.move"
        )
        self.outcode_select_move_single_arrow = page.locator(
            "#outcodeSelection div.box1 button.move"
        )
        self.excluded_outcode_filter = page.locator(
            "#outcodeSelection div.box1 input.filter"
        )
        self.excluded_gp_practice_groups_arrow = page.locator(
            "#gpPracticeGroupSelection div.box1 button.move"
        )
        self.excluded_outcode_groups_arrow = page.locator(
            "#outcodeGroupSelection div.box1 button.move"
        )
        self.excluded_gp_practices_list = page.locator(
            "select#bootstrap-duallistbox-nonselected-list_selectedGpPracticeCodes"
        )
        self.excluded_outcode_list = page.locator(
            "select#bootstrap-duallistbox-nonselected-list_selectedOutcodes"
        )
        self.excluded_gp_practice_groups = page.locator(
            "select#bootstrap-duallistbox-nonselected-list_selectedGpPracticeGroups"
        )
        self.excluded_outcode_groups = page.locator(
            "select#bootstrap-duallistbox-nonselected-list_selectedOutcodeGroups"
        )
        self.batch_title = page.locator("input#title")
        self.bso_batch_id_filter_text_box = page.locator(
            "#batchIdFilter input[type='text']"
        )
        self.specify_by_gp_practice_group_radio_btn = page.locator(
            "#include_specified_practice_groups"
        )
        self.specify_by_outcode_group_radio_btn = page.locator(
            "#include_specified_outcode_groups"
        )

    def enter_bso_batch_id(self, bso_batch_id: str) -> NiRiSpBatchPage:
        self.bso_batch_id_input.fill(bso_batch_id)

    def select_specify_by_gp_practice_group(self) -> NiRiSpBatchPage:
        self.specify_by_gp_practice_group_radio_btn.check()

    def select_specify_by_outcode_group(self) -> NiRiSpBatchPage:
        self.specify_by_outcode_group_radio_btn.check()

    def enter_batch_title(self, batch_title: str) -> NiRiSpBatchPage:
        self.batch_title.fill(batch_title)

    def enter_excluded_gp_practices_filter(self, text: str) -> NiRiSpBatchPage:
        self.excluded_gp_practices_filter.type(text)

    def select_excluded_gp_practices_from_list(self, gp_code: str) -> NiRiSpBatchPage:
        self.excluded_gp_practices_list.locator(f'option[value="{gp_code}"]').click()

    def select_excluded_outcodes_from_list(self, outcode: str) -> NiRiSpBatchPage:
        self.excluded_outcode_list.locator(f'option[value="{outcode}"]').click()

    def select_excluded_gp_practice_groups(self, gp_code: str) -> NiRiSpBatchPage:
        self.excluded_gp_practice_groups.locator(f'option[value="{gp_code}"]').click()

    def select_excluded_outcode_groups(self, outcode: str) -> NiRiSpBatchPage:
        self.excluded_outcode_groups.locator(f'option[value="{outcode}"]').click()

    def click_gp_practices_select_move(self) -> NiRiSpBatchPage:
        self.gp_practices_select_move_single_arrow.click()

    def click_gp_practice_groups_select_move(self) -> NiRiSpBatchPage:
        self.excluded_gp_practice_groups_arrow.click()

    def click_outcode_groups_select_move(self) -> NiRiSpBatchPage:
        self.excluded_outcode_groups_arrow.click()

    def enter_excluded_outcodes_filter(self, text: str) -> NiRiSpBatchPage:
        self.excluded_outcode_filter.fill(text)

    def click_outcodes_select_move(self) -> NiRiSpBatchPage:
        self.outcode_select_move_single_arrow.click()

    def enter_date_for_selection(self, days_offset: int) -> NiRiSpBatchPage:
        target_date = (datetime.today() + timedelta(days=days_offset)).strftime(
            "%d-%b-%Y"
        )
        self.selection_date_input.fill(target_date)

    def select_ntd_end_date(self, days_offset: int) -> NiRiSpBatchPage:
        target_date = (datetime.today() + timedelta(days=days_offset)).strftime(
            "%d-%b-%Y"
        )
        self.page.locator("#ntdEndDate").fill(target_date)

    def select_range_by_age(self) -> NiRiSpBatchPage:
        self.page.locator("input#include_age").check()

    def select_include_specified_practices(self) -> NiRiSpBatchPage:
        self.include_specified_practices_radio_btn.check()

    def select_include_specified_practice_groups(self) -> NiRiSpBatchPage:
        self.include_specified_practice_groups_radio_btn.check()

    def select_include_specified_outcodes(self) -> NiRiSpBatchPage:
        self.include_specified_outcodes_radio_btn.check()

    def select_include_specified_outcode_groups(self) -> NiRiSpBatchPage:
        self.include_specified_outcode_groups_radio_btn.check()

    def enter_include_year_of_birth_from(
        self, year_of_birth_from: str
    ) -> NiRiSpBatchPage:
        self.year_of_birth_from_input.fill(year_of_birth_from)

    def enter_ntdd_start_age_year(self, start_age: str) -> NiRiSpBatchPage:
        self.page.locator("#startAgeYears").fill(start_age)

    def enter_ntdd_end_age_year(self, end_age: str) -> NiRiSpBatchPage:
        self.page.locator("#endAgeYears").fill(end_age)

    def enter_ntdd_start_age_month(self, start_age: str) -> NiRiSpBatchPage:
        self.page.locator("#startAgeMonths").fill(start_age)

    def enter_ntdd_end_age_month(self, end_age: str) -> NiRiSpBatchPage:
        self.page.locator("#endAgeMonths").fill(end_age)

    def check_include_younger_women(self) -> NiRiSpBatchPage:
        check_box = self.page.locator("input#includeYoungerSubjects")
        check_box.check()
        assert check_box.is_checked()

    def enter_include_year_of_birth_to(self, year_of_birth_to: str) -> NiRiSpBatchPage:
        self.year_of_birth_to_input.fill(year_of_birth_to)

    def enter_include_month_of_birth_to(
        self, month_of_birth_to: str
    ) -> NiRiSpBatchPage:
        self.month_of_birth_to_input.fill(month_of_birth_to)

    def click_count_button(self) -> NiRiSpBatchPage:
        self.count_button.click()
        self.page.wait_for_timeout(3000)

    def assert_text_visible(self, text: str) -> NiRiSpBatchPage:
        locator = self.page.locator(f"p:has-text('{text}')")
        locator.scroll_into_view_if_needed()
        expect(locator).to_be_visible()

    def assert_page_header(self, expected_header: str) -> NiRiSpBatchPage:
        expect(self.page_heading).to_have_text(expected_header)

    def assert_global_error(self, expected_error: str) -> NiRiSpBatchPage:
        error_locator = self.page.locator("#globalErrorMessages li")
        expect(error_locator).to_contain_text(expected_error)

    def assert_entered_bso_batch_id_and_filtered_row_value(
        self, bso_batch_id: str
    ) -> NiRiSpBatchPage:
        self.bso_batch_id_filter_text_box.fill(bso_batch_id)
        self.page.wait_for_timeout(3000)
        first_row_second_cell_value = self.page.locator(
            "//tbody/tr[1]/td[2]"
        ).text_content()
        assert bso_batch_id == first_row_second_cell_value

    def search_by_batch_title(self, batch_title: str) -> NiRiSpBatchPage:
        self.page.locator("#batchTitleFilter input[type='text']").fill(batch_title)
        self.page.wait_for_timeout(2000)
        filtered_cell_value = self.page.locator("//tbody/tr[1]/td[11]").text_content()
        assert batch_title == filtered_cell_value

    def search_by_bso_batch_id_and_batch_title(
        self, bso_batch_id: str, batch_title: str
    ) -> NiRiSpBatchPage:
        self.bso_batch_id_filter_text_box.fill(bso_batch_id)
        self.search_by_batch_title(batch_title)
        self.page.wait_for_timeout(3000)
        first_row_second_cell_value = self.page.locator(
            "//tbody/tr[1]/td[2]"
        ).text_content()
        assert bso_batch_id == first_row_second_cell_value

    def assert_select_date_cell_value_is_not_null(
        self, cell_value: str
    ) -> NiRiSpBatchPage:
        self.page.wait_for_timeout(2000)
        select_date_cell_value = self.page.locator("//tbody/tr[1]/td[6]").text_content()
        assert select_date_cell_value.strip() != cell_value

    def assert_select_date_cell_value(self, cell_value: str) -> NiRiSpBatchPage:
        self.page.wait_for_timeout(2000)
        select_date_cell_value = self.page.locator("//tbody/tr[1]/td[6]").text_content()
        assert select_date_cell_value == cell_value

    def select_ri_sp_yob_from_drop_down(self) -> NiRiSpBatchPage:
        self.page.locator("#batchTypeList").select_option(label="RISP by Year of Birth")

    def select_ntdd_from_drop_down(self) -> NiRiSpBatchPage:
        self.page.locator("#batchTypeList").select_option(label="NTDD")

    def select_no_from_failsafe_flag_drop_down(self) -> NiRiSpBatchPage:
        self.page.locator("#failsafeFlagList").select_option(label="No")

    def click_count_select_button(self) -> NiRiSpBatchPage:
        select_btn = self.page.locator("#selectButton")
        confirm_btn_pop_up = self.page.locator("#confirmButtonInSelectPopupText")
        select_btn.click()
        confirm_btn_pop_up.click()
        self.page.wait_for_timeout(3000)

    def assert_selected_cell_value(self, cell_value: str) -> NiRiSpBatchPage:
        self.page.wait_for_timeout(2000)
        selected_cell_value = self.page.locator("//tbody/tr[1]/td[7]").text_content()
        assert selected_cell_value == cell_value

    def assert_selected_cell_value_is_not_null(
        self, cell_value: str
    ) -> NiRiSpBatchPage:
        self.page.wait_for_timeout(2000)
        selected_cell_value = self.page.locator("//tbody/tr[1]/td[7]").text_content()
        assert selected_cell_value.strip() != cell_value

    def assert_rejected_cell_value(self, cell_value: str) -> NiRiSpBatchPage:
        self.page.wait_for_timeout(2000)
        rejected_cell_value = self.page.locator("//tbody/tr[1]/td[8]").text_content()
        assert rejected_cell_value == cell_value

    def assert_rejected_cell_value_is_not_null(
        self, cell_value: str
    ) -> NiRiSpBatchPage:
        self.page.wait_for_timeout(2000)
        rejected_cell_value = self.page.locator("//tbody/tr[1]/td[8]").text_content()
        assert rejected_cell_value.strip() != cell_value

    def validate_batch_id_error(self, batch_id: str, expected_error: str) -> None:
        self.enter_bso_batch_id(batch_id)
        self.enter_date_for_selection(5)
        self.click_count_button()
        if "already exists" in expected_error:
            self.assert_global_error(expected_error)
        else:
            self.assert_text_visible(expected_error)

    def enter_year_range_and_count(
        self, from_year: str, to_year: str
    ) -> NiRiSpBatchPage:
        self.enter_bso_batch_id("PMA916865R")
        self.enter_date_for_selection(5)
        self.enter_include_year_of_birth_from(from_year)
        self.enter_include_year_of_birth_to(to_year)
        self.click_count_button()

    def verify_table_sort(self, column_header, sort_type, table: TableUtils, column_index, ascending) -> None:
        sort_order = "ascending" if ascending else "descending"
        table.go_to_first_page()
        self.page.click(f'//th[text()="{column_header}"]')
        self.page.wait_for_timeout(2000)
        ScreenshotTool(self.page).take_screenshot(f"additional_testing_TC_5_{column_header}_{sort_order}")
        all_data = table.get_all_table_data(column_index)
        # Normalize values if column is "Batch Title"
        if column_header == "Batch Type":
            all_data = ["Failsafe" if val == "Routine Failsafe" else val for val in all_data]
        logging.info(f"All {sort_order} data for {column_header}: {all_data}")
        assert table.is_sorted(all_data, sort_type, ascending=ascending), \
            f"{column_header} not sorted {sort_order} across all pages"

    def select_gp_practice_in_any_bso_radio_btn(self, gp_practice_code:str) -> None:
        # select gp practice in any bso under search batches
        self.page.locator("#include_gp_practice").click()
        # enter gp practice code in the text box
        self.page.locator("#gpPracticeCode").fill(gp_practice_code)

    def select_gp_practice_group_in_this_bso_radio_btn(self, gp_practice_group:str) -> None:
        # select gp practice group in this bso under search batches
        self.page.locator("#include_gp_practice_group").click()
        # enter gp practice group name in the text box
        self.page.locator("#gpPracticeGroupSearch").fill(gp_practice_group)

    def select_outcode_in_any_bso_radio_btn(self, outcode:str) -> None:
        # select outcode in any bso under search batches
        self.page.locator("#include_outcode").click()
        # enter outcode in the text box
        self.page.locator("#outcode").fill(outcode)

    def select_outcode_group_in_this_bso_radio_btn(self, outcode_group:str) -> None:
        # select outcode group in this bso under search batches
        self.page.locator("#include_outcode_group").click()
        # enter outcode group name in the text box
        self.page.locator("#outcodeGroupSearch").fill(outcode_group)

    def select_all_batches_in_this_bso_radio_btn(self) -> None:
        # select all batches in this bso under search batches
        self.page.locator("#include_all_batches").click()

    def click_on_search_btn_in_search_batches(self, bso_batch_id:str, batch_title:str) -> None:
        self.page.locator("#reportButton").click()
        self.page.wait_for_timeout(1000)
        self.page.locator("#batchIdFilter > input").fill(bso_batch_id)
        self.page.locator("#batchTitleFilter > input").fill(batch_title)
        self.page.wait_for_timeout(2000)

    def assert_bso_batch_id(self, expected_id: str, should_exist: bool = True):
        # Locator for all rows in the BSO Batch ID column
        bso_batch_ids = self.page.locator("//table/tbody//tr/td[1]")
        # Extract text contents of all matching cells
        values = bso_batch_ids.all_text_contents()
        # Print for debug
        logging.info(f"Found BSO IDs: {values}")
        if should_exist:
            assert expected_id in values, f"{expected_id} not found in BSO Batch ID column"
        else:
            assert expected_id not in values, f"{expected_id} *was found* in BSO Batch ID column, but it should not be."
            assert "No matching records found" in values
