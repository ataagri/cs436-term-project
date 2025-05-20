#!/bin/bash

# Exit on any error
set -e

# First, check if the image is accessible
echo "Verifying image exists..."
if ! docker pull gcr.io/cs436-reactfastcontacts/contacts-backend:latest > /dev/null 2>&1; then
  echo "❌ Error: Image not found. Run build_and_push.sh first."
  exit 1
fi

# Apply the deployment
echo "Updating Kubernetes deployment..."
kubectl apply -f backend-deployment-amd64.yaml

# Scale down the older deployment
echo "Scaling down the old deployment..."
kubectl scale deployment contacts-backend --replicas=0

# Delete the older deployment if needed
read -p "Do you want to delete the old deployment? (y/n): " choice
if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
  kubectl delete deployment contacts-backend
  echo "Old deployment deleted."
else
  echo "Old deployment kept but scaled to 0 replicas."
fi

# Check the status
echo "Checking deployment status..."
kubectl rollout status deployment contacts-backend-amd64

echo "✅ Deployment updated successfully"