#!/bin/bash

# Set a minimum coverage percentage threshold
MIN_COVERAGE=80

source ./.venv/bin/activate
cd ./src
coverage run -m unittest discover -s ./tests
TEST_STATUS=$?
coverage report -m --fail-under=$MIN_COVERAGE
COVERAGE_STATUS=$?
deactivate

# Exit with a non-zero status if tests failed or coverage is below the threshold
if [[ $TEST_STATUS -ne 0 ]]; then
    echo "Tests failed with status $TEST_STATUS."
    exit 1
elif [[ $COVERAGE_STATUS -ne 0 ]]; then
    echo "Coverage is below the threshold of $MIN_COVERAGE%."
    exit 1
else
    echo "All tests passed and coverage meets the threshold."
    exit 0
fi
