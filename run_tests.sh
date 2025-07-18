#!/bin/bash

BASE_URL=$1
MARKERS_TO_USE="${2//-/ }" # replace hyphens with spaces
MARKERS_TO_USE=$(echo "$MARKERS_TO_USE" | sed -E 's/\b([A-Z]+) ([0-9]{4})\b/\1-\2/') # replace space in Jira ticket number(s) with hyphen
echo "here"
echo $MARKERS_TO_USE
export COGNITO_USER_PASSWORD=$3

pytest --tracing retain-on-failure --base-url $BASE_URL -m "$MARKERS_TO_USE"
