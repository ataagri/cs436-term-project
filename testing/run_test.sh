#!/bin/bash

# Script to run Locust tests with different configurations

# Make sure the script is executable
# chmod +x run_test.sh

# Install Locust if not already installed
echo "Checking if Locust is installed..."
if ! command -v locust &> /dev/null; then
    echo "Installing Locust..."
    pip install locust
fi

# Function to run a test with specific parameters
run_test() {
    local users=$1
    local spawn_rate=$2
    local run_time=$3
    local test_name=$4
    
    echo "Running test: $test_name with $users users, spawn rate $spawn_rate, for $run_time"
    
    # Create a directory for this test's results
    mkdir -p "results/$test_name"
    
    # Run Locust in headless mode with CSV output
    locust --locustfile locustfile.py \
           --host https://api.ataagri.com \
           --users $users \
           --spawn-rate $spawn_rate \
           --run-time $run_time \
           --headless \
           --csv="results/$test_name/stats" \
           --html="results/$test_name/report.html"
    
    echo "Test completed. Results saved to results/$test_name/"
}

# Create results directory
mkdir -p results

# Run a series of tests with increasing load
echo "Starting load testing sequence..."

# Test 1: Baseline - Low load
run_test 10 2 2m "baseline"

# Test 2: Medium load
run_test 50 5 5m "medium_load"

# Test 3: High load - should trigger autoscaling
run_test 200 10 10m "high_load"

# Test 4: Spike test - rapid increase in users
run_test 300 50 5m "spike_test"

# Test 5: Endurance test - moderate load for longer period
run_test 100 10 15m "endurance_test"

echo "All tests completed. Check the 'results' directory for detailed reports."
