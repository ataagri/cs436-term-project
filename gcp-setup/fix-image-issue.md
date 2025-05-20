# Fix Backend Image Architecture Issue

The current deployment is failing because the Docker image was built on an ARM64 architecture (likely an M1/M2 Mac) but is trying to run on AMD64 architecture in GKE. Here's a comprehensive guide to fix this issue.

## Option 1: Build and Push from Google Cloud Shell

The most reliable way to ensure architecture compatibility is to build the image directly on Google Cloud:

1. Open Google Cloud Shell (it uses AMD64 architecture)

2. Clone your repository:
   ```bash
   git clone <your-repo-url>
   cd cs436-term-project/backend
   ```

3. Build and push the image:
   ```bash
   docker build -t gcr.io/cs436-reactfastcontacts/contacts-backend:latest .
   docker push gcr.io/cs436-reactfastcontacts/contacts-backend:latest
   ```

4. Update the deployment:
   ```bash
   kubectl rollout restart deployment contacts-backend
   ```

## Option 2: Use Docker BuildX with Explicit Platform Target

If you prefer to build locally:

1. Create a Docker BuildX builder with platform capabilities:
   ```bash
   docker buildx create --name amd64-builder --use
   docker buildx inspect --bootstrap
   ```

2. Build and push with platform specification:
   ```bash
   cd backend
   docker buildx build --platform=linux/amd64 \
     -t gcr.io/cs436-reactfastcontacts/contacts-backend:latest \
     --push .
   ```

3. Update the deployment:
   ```bash
   kubectl rollout restart deployment contacts-backend
   ```

## Option 3: Use Google Cloud Build

Let Google Cloud build the image with the correct architecture:

1. Create a cloudbuild.yaml file:
   ```yaml
   steps:
   - name: 'gcr.io/cloud-builders/docker'
     args: ['build', '-t', 'gcr.io/cs436-reactfastcontacts/contacts-backend:latest', '.']
   images:
   - 'gcr.io/cs436-reactfastcontacts/contacts-backend:latest'
   ```

2. Run the build:
   ```bash
   cd backend
   gcloud builds submit --config=cloudbuild.yaml .
   ```

3. Update the deployment:
   ```bash
   kubectl rollout restart deployment contacts-backend
   ```

## Fix the Backend Service

After successfully updating the image, you'll need to ensure your service points to the correct deployment:

1. Check the current service:
   ```bash
   kubectl get service contacts-backend
   ```

2. If needed, update the service to target the right selector:
   ```bash
   kubectl edit service contacts-backend
   ```
   
   Ensure the selector matches your deployment's labels (usually `app: contacts-backend`).

## Verify the Fix

1. Check that pods are running:
   ```bash
   kubectl get pods -l app=contacts-backend
   ```

2. Check the logs for any errors:
   ```bash
   kubectl logs -l app=contacts-backend
   ```

3. Test the API endpoint:
   ```bash
   curl https://api.cs436-reactfastcontacts.com/health
   ```

Remember to revert any temporary changes to your deployment files after fixing the issue.