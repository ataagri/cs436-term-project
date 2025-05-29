#!/bin/bash

# Create a directory for test results
mkdir -p testing/pod-config-results

# Function to run tests with a specific configuration
test_configuration() {
  config_name=$1
  deployment_file=$2
  
  echo "===== Testing $config_name configuration ====="
  
  # Create a directory for this configuration's results
  mkdir -p "testing/pod-config-results/$config_name"
  
  # Apply the deployment configuration
  echo "Applying $deployment_file..."
  kubectl apply -f "$deployment_file"
  
  # Wait for deployment to stabilize
  echo "Waiting for deployment to stabilize..."
  kubectl rollout status deployment/contacts-backend-latest
  
  # Wait an additional 30 seconds to ensure everything is ready
  sleep 30
  
  # Run the load tests
  echo "Running load tests..."
  cd testing
  
  # Run baseline test
  ./run_test.sh
  
  # Copy results to the configuration directory
  cp -r results/* "pod-config-results/$config_name/"
  
  # Return to the project root
  cd ..
  
  echo "===== Completed testing $config_name configuration ====="
}

# Test each configuration
test_configuration "small" "kubernetes/test-configs/small-deployment.yaml"
test_configuration "medium" "kubernetes/test-configs/medium-deployment.yaml"
test_configuration "large" "kubernetes/test-configs/large-deployment.yaml"

# Restore the original configuration
kubectl apply -f kubernetes/backend-deployment-latest.yaml

echo "All tests completed. Results are in testing/pod-config-results/"
