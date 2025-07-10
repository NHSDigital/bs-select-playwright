#!/bin/bash

MARKERS_TO_USE="${2//-/ }"
export COGNITO_USER_PASSWORD=$3

pytest --tracing retain-on-failure --base-url $1 -m "$MARKERS_TO_USE"
