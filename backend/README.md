# Backend Service for Contact Management App

This is the backend service for the React Fast Contacts application. It provides a REST API for managing contacts.

## Local Development

### Setup

1. Install dependencies:
   ```bash
   pipenv install
   ```

2. Start the local development server:
   ```bash
   ./run_local.sh
   ```

3. The API will be available at http://localhost:8000

## Cloud Deployment

### Building and Pushing the Docker Image

The application is deployed to Google Kubernetes Engine (GKE). Due to architecture differences between development machines (possibly ARM64) and GKE clusters (AMD64), you need to build a platform-specific Docker image.

To build and push the correct image:

```bash
./build_and_push.sh
```

This script:
1. Builds a Docker image targeting the AMD64 platform using Dockerfile.platform
2. Pushes the image to Google Container Registry
3. Provides instructions for updating the deployment

### Updating the Deployment

After pushing a new image, update the deployment:

```bash
kubectl rollout restart deployment contacts-backend
```

## Environment Variables

The service uses the following environment variables:

- `DB_USER`: Database username (from Kubernetes secret)
- `DB_PASSWORD`: Database password (from Kubernetes secret)
- `DB_NAME`: Database name (default: contacts)
- `DB_HOST`: Cloud SQL instance connection name or host

## API Endpoints

- `GET /contacts`: List all contacts
- `GET /contacts/{id}`: Get a specific contact
- `POST /contacts`: Create a new contact
- `PUT /contacts/{id}`: Update a contact
- `DELETE /contacts/{id}`: Delete a contact

## Architecture Notes

The service connects to a Cloud SQL PostgreSQL database using the Cloud SQL Proxy sidecar container in Kubernetes. This provides a secure connection to the database without exposing it to the public internet.