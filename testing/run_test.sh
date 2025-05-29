#!/bin/bash

# Script to run Locust tests for pod configuration testing

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

# Test 1: Low load
run_test 20 5 2m "low_load"

# Test 2: Medium load
run_test 100 10 5m "medium_load"

# Test 3: High load - should test resource limits
run_test 300 20 5m "high_load"

echo "All tests completed. Check the 'results' directory for detailed reports."
