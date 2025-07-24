#!/bin/bash

BASE_URL="$1"
ALL_MARKERS="$2"
export COGNITO_USER_PASSWORD="$3"

BRANCH_NAME="${ALL_MARKERS%%.*}" # taken from head of ALL_MARKERS
TRAILING_MARKERS="${ALL_MARKERS:$((${#BRANCH_NAME}))}" # everything in ALL_MARKERS that is not BRANCH_NAME
BRANCH_MARKER_TEMPLATE="branch(serial='%')"
BRANCH_MARKER="${BRANCH_MARKER_TEMPLATE//%/$BRANCH_NAME}" # interpolate BRANCH_NAME in to BRANCH_MARKER_TEMPLATE at %
COMBINED_MARKERS="$BRANCH_MARKER$TRAILING_MARKERS"
MARKERS_TO_USE="${COMBINED_MARKERS//./ }" # replace full stops with spaces

pytest --tracing retain-on-failure --base-url $BASE_URL -m "$MARKERS_TO_USE"
