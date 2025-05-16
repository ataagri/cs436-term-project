# GCP Project Setup

## 1. Create a New GCP Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click on "New Project"
4. Enter a project name (e.g., "contacts-app")
5. Select an organization (if applicable)
6. Click "Create"

## 2. Enable Required APIs

Enable the following APIs through the Google Cloud Console or using the gcloud command-line tool:

```bash
# Install Google Cloud SDK if not already installed
# See: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Set the project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable firebase.googleapis.com
gcloud services enable identitytoolkit.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

## 3. Set up Firebase for the Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Select your GCP project
4. Follow the setup wizard to complete the Firebase setup
5. Enable Authentication in the Firebase console
   - Go to "Authentication" > "Sign-in method"
   - Enable Email/Password provider

## 4. Set up Artifact Registry Repository

Create a Docker repository to store your container images:

```bash
# Create a Docker repository
gcloud artifacts repositories create contacts-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker repository for Contacts app"

# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker us-central1-docker.pkg.dev
```

## 5. Set up Service Accounts

Create service accounts with the necessary permissions:

```bash
# Create service account for GKE
gcloud iam service-accounts create gke-service-account \
    --display-name="GKE Service Account"

# Grant required roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:gke-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/container.developer"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:gke-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"
```

Replace `YOUR_PROJECT_ID` with your actual GCP project ID.