#!/bin/bash
# run_test.sh - Run integration tests for AI Writers Workshop

echo "Running AI Writers Workshop integration test..."

# Ensure virtual environment is activated
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the integration test
python tests/integration_test.py

# Deactivate virtual environment
deactivate

echo "Test completed!"
