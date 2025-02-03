#!/bin/bash

# Cleanup function to remove runner
cleanup() {
    echo "Removing runner..."
    ./config.sh remove --token "${GITHUB_TOKEN}"
    exit
}

# Set up the cleanup trap
trap cleanup SIGTERM SIGINT

# Configure the runner
./config.sh --url "${GITHUB_ORG_URL}" \
    --token "${GITHUB_TOKEN}" \
    --name "${RUNNER_NAME}" \
    --unattended \
    --replace \
    --ephemeral

# Start the runner and wait
./run.sh &
wait $! 