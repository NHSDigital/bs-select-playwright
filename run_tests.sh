#!/bin/bash

BASE_URL="$1"
ALL_MARKERS="$2"
export COGNITO_USER_PASSWORD="$3"

replace_full_stops_with_spaces() {
  local input_string="$1"
  echo "${input_string//./ }"
}

prepare_markers_containing_branch_name() {
  local all_markers="$1"
  local branch_name="${all_markers%%.*}" # taken from head of ALL_MARKERS. Branch name must be first if present.
  local trailing_markers="${all_markers:${#branch_name}}" # everything in ALL_MARKERS that is not branch_name
  local branch_marker_template="branch(serial='%')"
  local branch_marker="${branch_marker_template//%/$branch_name}" # interpolate branch_name in to branch_marker_template at %
  local combined_markers="$branch_marker$trailing_markers"
  echo "$(replace_full_stops_with_spaces "$combined_markers")"
}

# if there are no markers (all tests will run)
if [[ -z "$ALL_MARKERS" ]]; then
  MARKERS_TO_USE=""

# if a hyphen is present then at least one of the markers is a branch name
# e.g. "bss2-2402", "bss2-2402.or.smoke"
elif [[ "$ALL_MARKERS" =~ \- ]]; then
  MARKERS_TO_USE="$(prepare_markers_containing_branch_name "$ALL_MARKERS")"

# if a full stop is present there are multiple markers separated by full stops
# e.g. "smoke.or.release"
elif [[ "$ALL_MARKERS" =~ \. ]]; then
  MARKERS_TO_USE="$(replace_full_stops_with_spaces "$ALL_MARKERS")"

# a single non-branch name marker is present
# e.g. "smoke"
else
  MARKERS_TO_USE=$ALL_MARKERS
fi

pytest --tracing retain-on-failure --base-url "$BASE_URL" -m "$MARKERS_TO_USE"
