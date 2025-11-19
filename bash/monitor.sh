#!/bin/bash

# Maximum allowed runtime in seconds
MAX_RUNTIME=120  # Change this to your desired limit

# Check every 5 seconds
INTERVAL=5

while true; do
    echo "Checking for long-running processes..."

    # Loop through all running processes
    for pid in $(ps -e -o pid --no-headers); do
        # Get the elapsed time in seconds
        ELAPSED=$(ps -p $pid -o etimes=)

        # Check if elapsed time exceeds the max runtime
        if [ "$ELAPSED" -gt "$MAX_RUNTIME" ]; then
            # Get process details
            PROC_NAME=$(ps -p $pid -o comm=)
            echo "Killing long-running process: $PROC_NAME (PID $pid) - Runtime: ${ELAPSED}s"
            kill -9 $pid
        fi
    done

    # Sleep before checking again
    sleep $INTERVAL
done
