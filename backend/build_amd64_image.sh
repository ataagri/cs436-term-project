#!/bin/bash
set -e

# Project settings
PROJECT_ID="cs436-reactfastcontacts"
IMAGE_NAME="contacts-backend"
IMAGE_TAG="amd64"
FULL_IMAGE_NAME="gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "Building AMD64 Docker image..."

# Build using explicit platform flag and the amd64-specific Dockerfile
docker buildx build --platform=linux/amd64 -f Dockerfile.amd64 -t ${FULL_IMAGE_NAME} --push .

echo "✅ Successfully built and pushed ${FULL_IMAGE_NAME}"
echo ""
echo "Now update your deployment to use this image:"
echo "Edit kubernetes/backend-deployment-amd64.yaml to use: ${FULL_IMAGE_NAME}"
echo "Then run: kubectl apply -f kubernetes/backend-deployment-amd64.yaml"