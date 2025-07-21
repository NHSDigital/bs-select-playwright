#!/bin/bash

BASE_URL="$1"
ALL_MARKERS="$2"
export COGNITO_USER_PASSWORD="$3"

BRANCH_NAME="${ALL_MARKERS##*.}" # taken from tail of ALL_MARKERS
LEADING_MARKERS="${ALL_MARKERS:0:$((${#ALL_MARKERS} - ${#BRANCH_NAME}))}" # taken from head of ALL_MARKERS
BRANCH_MARKER_TEMPLATE="branch(serial='%')"
BRANCH_MARKER="${BRANCH_MARKER_TEMPLATE//%/$BRANCH_NAME}" # interpolate BRANCH_NAME in to BRANCH_MARKER_TEMPLATE at %
COMBINED_MARKERS="$LEADING_MARKERS$BRANCH_MARKER"
MARKERS_TO_USE="${COMBINED_MARKERS//./ }" # replace full stops with spaces

pytest --tracing retain-on-failure --base-url $BASE_URL -m "$MARKERS_TO_USE"
