#!/bin/sh

BASE_URL=${1:-${BASE_URL}}
MARKERS_TO_USE=${2:=${MARKERS_TO_USE}}
MARKERS_TO_USE="${MARKERS_TO_USE//-/ }"
export COGNITO_USER_PASSWORD=${3:=${COGNITO_USER_PASSWORD}}

pytest --tracing retain-on-failure -p no:warnings --base-url $BASE_URL -m "$MARKERS_TO_USE"
