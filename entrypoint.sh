#!/bin/bash
# entrypoint.sh

# Check if a script name is provided
if [ -z "$1" ]; then
    echo "No script provided, running fraud_detection.py by default."
    python fraud_detection.py
else
    echo "Running script: $1"
    python $1
fi
