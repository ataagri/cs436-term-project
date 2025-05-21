# ReactFast Contacts - Contact Management Application

![ReactFast Contacts](https://img.shields.io/badge/ReactFast-Contacts-009688.svg?style=for-the-badge)
[![React](https://img.shields.io/badge/react-35495e.svg?&style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TailwindCSS](https://img.shields.io/badge/tailwindcss-gray.svg?&style=for-the-badge&logo=tailwindcss&logoColor=06B6D4)](https://tailwindcss.com/)
[![FastAPI](https://img.shields.io/badge/fastapi-009688.svg?&style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Firebase](https://img.shields.io/badge/firebase-FFCA28.svg?&style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![Google Cloud](https://img.shields.io/badge/google_cloud-4285F4.svg?&style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-336791.svg?&style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-326CE5.svg?&style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)

A modern, production-ready contact management application built with React, FastAPI, and deployed on Google Cloud Platform.

## Live Demo

The application is currently deployed and accessible at:
- Frontend: [https://cs436-reactfastcontacts.web.app](https://cs436-reactfastcontacts.web.app)
- Backend API: [https://api.ataagri.com](https://api.ataagri.com)
- API Documentation: 
  - Swagger UI: [https://api.ataagri.com/docs](https://api.ataagri.com/docs)
  - ReDoc: [https://api.ataagri.com/redoc](https://api.ataagri.com/redoc)

## Table of Contents

- [Live Demo](#live-demo)
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Quick Start with Docker](#quick-start-with-docker-recommended)
  - [Manual Setup](#manual-setup-alternative)
  - [Cloud SQL Proxy Setup](#cloud-sql-proxy-setup-for-gcp-development)
  - [Monitoring Setup](#monitoring-setup)
- [Google Cloud Deployment](#google-cloud-deployment)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contact](#contact)

## Overview

ReactFast Contacts is a comprehensive contact management application that showcases a production-ready architecture using modern web technologies. It allows users to create, view, edit, and delete contacts through an intuitive interface with a mobile phone-like layout.

The application demonstrates best practices for cloud-native development, including containerization, orchestration, authentication, and monitoring. The frontend is deployed to Firebase Hosting, while the backend runs on Google Kubernetes Engine, with a PostgreSQL database on Cloud SQL.

## Features

### Contact Management
- **View All Contacts**: Browse through your entire contact list
- **Contact Details**: View detailed information for each contact
- **Add New Contacts**: Create new contacts with full details
- **Edit Contacts**: Update contact information
- **Delete Contacts**: Remove contacts you no longer need

### User Authentication
- **User Registration**: Create a new account with email and password
- **User Login**: Secure authentication using Firebase
- **Protected Routes**: Access to contacts only for authenticated users

### Cloud-Native Architecture
- **Horizontal Scaling**: Backend scales based on demand
- **Load Balancing**: Even distribution of traffic
- **Managed Database**: Cloud SQL for PostgreSQL
- **Monitoring**: Prometheus and Grafana dashboards

### Developer Experience
- **Local Development**: Easy setup for local development with Docker Compose
- **Containerization**: Docker support for consistent environments
- **Detailed Documentation**: Comprehensive setup and troubleshooting guides
- **Monitoring**: Built-in Prometheus and Grafana for local development

## Architecture

The application follows a modern cloud-native architecture with three primary layers:

### Frontend Layer
- React Single-Page Application (SPA)
- Hosted on Firebase Hosting
- Firebase Authentication for user management
- Communicates with backend via REST API
- Mobile-responsive design with Tailwind CSS

### API Layer
- FastAPI application running on GKE
- Horizontally scaled with Kubernetes
- Load balanced with Google Cloud Load Balancer
- Secured with SSL/TLS
- Prometheus instrumentation for monitoring

### Database Layer
- PostgreSQL on Cloud SQL
- Connected to backend via Cloud SQL Proxy
- Credentials managed securely with Kubernetes Secrets

### Infrastructure
- Containerization with Docker
- Orchestration with Kubernetes
- Autoscaling based on CPU and memory utilization
- Custom domain with TLS certificate
- Monitoring with Prometheus and Grafana

## Technology Stack

### Frontend
- **React**: JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework
- **Firebase Authentication**: User authentication service
- **React Router**: Navigation for React applications
- **Axios**: HTTP client for making API requests

### Backend
- **FastAPI**: Modern, high-performance Python web framework
- **SQLAlchemy**: SQL toolkit and ORM for Python
- **Prometheus FastAPI Instrumentator**: Metrics collection for FastAPI
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI

### Database
- **PostgreSQL**: Open-source relational database

### DevOps & Deployment
- **Docker**: Containerization platform
- **Kubernetes**: Container orchestration platform
- **Google Kubernetes Engine (GKE)**: Managed Kubernetes service
- **Cloud SQL**: Managed PostgreSQL database
- **Firebase Hosting**: Web application hosting
- **Firebase Cloud Functions**: Serverless functions for backend logic
- **Cloud Load Balancer**: Load balancing for traffic distribution
- **Prometheus & Grafana**: Monitoring and visualization

## Project Structure

```
/
├── frontend/                 # React frontend application
│   ├── public/               # Static files
│   ├── src/                  # Source code
│   │   ├── components/       # React components
│   │   │   ├── auth/         # Authentication components
│   │   │   ├── layouts/      # Layout components
│   │   │   └── base/         # Base components
│   │   ├── App.js            # Main application component
│   │   ├── firebase.js       # Firebase configuration
│   │   └── index.js          # Application entry point
│   ├── package.json          # NPM package configuration
│   ├── Dockerfile.dev        # Docker configuration for development
│   └── tailwind.config.js    # Tailwind CSS configuration
├── backend/                  # FastAPI backend application
│   ├── main.py               # FastAPI application entry point
│   ├── models.py             # SQLAlchemy models
│   ├── db.py                 # Database configuration
│   ├── create_db.py          # Database initialization script
│   ├── Dockerfile            # Docker configuration for backend
│   └── Pipfile               # Python dependencies
├── functions/                # Firebase Cloud Functions
│   ├── index.js              # Cloud Functions entry point
│   └── package.json          # Node.js dependencies
├── kubernetes/               # Kubernetes configuration files
│   ├── backend-deployment-latest.yaml # Backend deployment configuration
│   ├── backend-service.yaml  # Backend service configuration
│   ├── ingress.yaml          # Ingress configuration
│   ├── certificate.yaml      # SSL certificate configuration
│   ├── db-credentials.yaml   # Database credentials configuration
│   └── autoscale.yaml        # HPA configuration
├── prometheus/               # Prometheus configuration
│   └── prometheus.yml        # Prometheus configuration file
├── grafana/                  # Grafana configuration
│   └── provisioning/         # Grafana provisioning
│       ├── datasources/      # Prometheus datasource configuration
│       └── dashboards/       # Dashboard configurations
├── docker-compose.yml        # Docker Compose configuration for local development
├── setup.sh                  # Setup script for local development
└── README.md                 # Project documentation
```

## Setup and Installation

### Prerequisites

- Docker and Docker Compose (for the easiest setup)
- Alternatively:
  - Node.js (v16 or later)
  - Python (v3.9 or later)
  - PostgreSQL (v13 or later)
  - Firebase account (for authentication)
  - Google Cloud SDK (for deployment)
  - kubectl (for Kubernetes deployment)

### Quick Start with Docker (Recommended)

The easiest way to get started is using Docker Compose, which sets up the entire application stack including:
- PostgreSQL database
- FastAPI backend
- React frontend
- Prometheus monitoring
- Grafana dashboards

1. Run the setup script:
   ```bash
   ./setup.sh
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001 (login: admin/password)

3. To stop the application:
   ```bash
   docker-compose down
   ```

### Manual Setup (Alternative)

If you prefer to set up each component individually, follow these steps:

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Create a `.env.local` file from the example:
   ```bash
   cp .env.local.example .env.local
   ```

3. Edit `.env.local` with your settings:
   ```
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_USE_AUTH=false  # Set to true if using Firebase auth
   ```

4. If using authentication, set up Firebase:
   - Create a project at https://console.firebase.google.com/
   - Enable Authentication with Email/Password provider
   - Add your Firebase configuration to `.env.local`

5. Install dependencies and start the development server:
   ```bash
   npm install
   npm start
   ```

6. The frontend will be available at `http://localhost:3000`

#### Database Setup

1. Install and start PostgreSQL or use Docker:
   ```bash
   docker run --name contacts-db \
     -e POSTGRES_PASSWORD=localpassword \
     -e POSTGRES_USER=contacts-user \
     -e POSTGRES_DB=contacts \
     -p 5432:5432 \
     -d postgres:13
   ```

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies using Pipenv:
   ```bash
   pip install pipenv
   pipenv install
   ```

3. Set up environment variables for local development:
   ```bash
   export DB_USER=contacts-user
   export DB_PASSWORD=localpassword
   export DB_NAME=contacts
   export DB_HOST=localhost
   export DB_PORT=5432
   export CLOUD_SQL_PROXY=false
   ```

4. Initialize the database:
   ```bash
   pipenv run python create_db.py
   ```

5. Start the development server:
   ```bash
   pipenv run uvicorn main:app --reload
   ```

6. The API will be available at `http://localhost:8000`

### Cloud SQL Proxy Setup (For GCP Development)

If you want to connect to a Cloud SQL instance for development:

1. Download the Cloud SQL Proxy:
   ```bash
   # For macOS
   curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.0.0/cloud-sql-proxy.darwin.amd64
   chmod +x cloud-sql-proxy
   
   # For Linux
   curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.0.0/cloud-sql-proxy.linux.amd64
   chmod +x cloud-sql-proxy
   
   # For Windows (using PowerShell)
   Invoke-WebRequest -Uri "https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.0.0/cloud-sql-proxy.windows.amd64.exe" -OutFile "cloud-sql-proxy.exe"
   ```

2. Authenticate with Google Cloud:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. Start the Cloud SQL Proxy:
   ```bash
   ./cloud-sql-proxy --instances=YOUR_PROJECT_ID:REGION:INSTANCE_NAME=tcp:5432
   ```

4. Configure the backend to use the proxy:
   ```bash
   export DB_USER=your_cloud_sql_user
   export DB_PASSWORD=your_cloud_sql_password
   export DB_NAME=contacts
   export DB_HOST=localhost
   export DB_PORT=5432
   export CLOUD_SQL_PROXY=true
   ```

### Monitoring Setup

The Docker Compose setup includes Prometheus and Grafana for monitoring. If you're setting up manually:

1. Install Prometheus and configure it to scrape the `/metrics` endpoint of the backend
2. Install Grafana and configure it to use Prometheus as a data source
3. Import dashboards for FastAPI monitoring

## Google Cloud Deployment

The application is designed to be deployed to Google Cloud Platform using a production-ready architecture. The deployment process involves several key steps:

### GCP Project and Infrastructure Setup

1. Create a new GCP project and enable required APIs:
   ```bash
   # Create a new project
   gcloud projects create YOUR_PROJECT_ID --name="ReactFast Contacts"
   
   # Set the project as active
   gcloud config set project YOUR_PROJECT_ID
   
   # Enable required APIs
   gcloud services enable compute.googleapis.com \
     container.googleapis.com \
     sqladmin.googleapis.com \
     cloudbuild.googleapis.com \
     containerregistry.googleapis.com \
     firebase.googleapis.com
   ```

2. Set up Firebase project:
   - Go to the [Firebase Console](https://console.firebase.google.com/)
   - Add a project and select your GCP project
   - Enable Authentication with Email/Password provider:
     - Go to Authentication > Sign-in method
     - Enable Email/Password provider
   - Register your app to get the Firebase config

3. Configure service accounts with appropriate permissions:
   ```bash
   # Create a service account for Cloud SQL
   gcloud iam service-accounts create cloud-sql-proxy \
     --display-name="Cloud SQL Proxy"
   
   # Assign necessary roles
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:cloud-sql-proxy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/cloudsql.client"
   ```

### Database Deployment

1. Create a PostgreSQL instance on Cloud SQL:
   ```bash
   gcloud sql instances create contacts-db \
     --database-version=POSTGRES_13 \
     --tier=db-f1-micro \
     --region=us-central1 \
     --storage-type=SSD \
     --storage-size=10GB \
     --root-password=YOUR_ROOT_PASSWORD
   ```

2. Create database and user:
   ```bash
   gcloud sql databases create contacts --instance=contacts-db
   
   gcloud sql users create contacts-user \
     --instance=contacts-db \
     --password=YOUR_USER_PASSWORD
   ```

3. Note your instance connection name:
   ```bash
   gcloud sql instances describe contacts-db --format='value(connectionName)'
   # Output will be something like: your-project-id:us-central1:contacts-db
   ```

### Backend Deployment

1. Update Kubernetes secrets with your database credentials:
   ```bash
   # Edit the db-credentials.yaml file with your actual credentials
   # Then apply it
   kubectl apply -f kubernetes/db-credentials.yaml
   ```

2. Build and push the Docker image:
   ```bash
   cd backend
   
   # Build the image
   docker build -t gcr.io/YOUR_PROJECT_ID/contacts-backend:latest .
   
   # Configure Docker to use gcloud credentials
   gcloud auth configure-docker
   
   # Push the image
   docker push gcr.io/YOUR_PROJECT_ID/contacts-backend:latest
   ```

3. Create a GKE cluster:
   ```bash
   gcloud container clusters create contacts-cluster \
     --zone us-central1-a \
     --num-nodes 3 \
     --machine-type e2-standard-2
   ```

4. Get credentials for kubectl:
   ```bash
   gcloud container clusters get-credentials contacts-cluster --zone us-central1-a
   ```

5. Update the Kubernetes deployment files:
   - Edit `kubernetes/backend-deployment-latest.yaml` to use your project ID
   - Edit `kubernetes/ingress.yaml` to use your domain name

6. Deploy to Kubernetes:
   ```bash
   kubectl apply -f kubernetes/db-credentials.yaml
   kubectl apply -f kubernetes/backend-deployment-latest.yaml
   kubectl apply -f kubernetes/backend-service.yaml
   kubectl apply -f kubernetes/certificate.yaml
   kubectl apply -f kubernetes/ingress.yaml
   kubectl apply -f kubernetes/autoscale.yaml
   ```

### Frontend Deployment

1. Update the Firebase configuration in the frontend:
   ```bash
   # Create a production environment file
   cd frontend
   cp .env.local.example .env.production
   ```

2. Edit `.env.production` with your production settings:
   ```
   REACT_APP_API_URL=https://your-api-domain.com
   REACT_APP_USE_AUTH=true
   REACT_APP_FIREBASE_API_KEY=your_api_key
   # Add all other Firebase config values
   ```

3. Install and configure Firebase CLI:
   ```bash
   npm install -g firebase-tools
   firebase login
   firebase use YOUR_PROJECT_ID
   ```

4. Build and deploy to Firebase Hosting:
   ```bash
   npm run build
   firebase deploy --only hosting
   ```

### Cloud Functions Deployment (Optional)

1. Update Firebase functions configuration:
   ```bash
   cd functions
   npm install
   ```

2. Deploy Firebase Cloud Functions:
   ```bash
   firebase deploy --only functions
   ```

### Monitoring Setup

1. Set up a VM for Prometheus and Grafana:
   ```bash
   gcloud compute instances create monitoring-vm \
     --zone=us-central1-a \
     --machine-type=e2-medium \
     --image-family=debian-10 \
     --image-project=debian-cloud
   ```

2. SSH into the VM and install Docker:
   ```bash
   gcloud compute ssh monitoring-vm --zone=us-central1-a
   
   # Install Docker and Docker Compose
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose
   sudo usermod -aG docker $USER
   ```

3. Create monitoring configuration files similar to the local setup

4. Start the monitoring stack:
   ```bash
   docker-compose up -d
   ```

5. Configure firewall rules to access Grafana:
   ```bash
   gcloud compute firewall-rules create allow-grafana \
     --allow tcp:3000 \
     --target-tags=monitoring-vm \
     --description="Allow Grafana web interface"
   ```

#### Metrics Endpoint

The application provides a Prometheus-compatible metrics endpoint at `/metrics` that exposes:

- HTTP request counts, durations, and sizes by handler and method
- Python garbage collection statistics
- Process information (memory usage, CPU time, etc.)

These metrics can be scraped by Prometheus and visualized in Grafana dashboards to monitor:

- API performance and latency
- Request volume and patterns
- Resource utilization
- Error rates

Example metrics available:
```
http_requests_total - Total number of HTTP requests
http_request_duration_seconds - Request latency
process_resident_memory_bytes - Memory usage
process_cpu_seconds_total - CPU usage
```

## API Documentation

The FastAPI backend provides automatic API documentation. You can access:

- **Live API Documentation**:
  - Swagger UI: [https://api.ataagri.com/docs](https://api.ataagri.com/docs)
  - ReDoc: [https://api.ataagri.com/redoc](https://api.ataagri.com/redoc)

- **Local Development Documentation**:
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`

### Endpoints

| Method | URL                   | Description                         |
|--------|------------------------|-------------------------------------|
| GET    | /                      | Health check                        |
| GET    | /health                | Detailed health check               |
| GET    | /metrics               | Prometheus metrics endpoint         |
| GET    | /contacts              | Get all contacts                    |
| GET    | /contacts/{contact_id} | Get a specific contact              |
| POST   | /contacts              | Create a new contact                |
| PATCH  | /contacts/{contact_id} | Update an existing contact          |
| DELETE | /contacts/{contact_id} | Delete a contact                    |

### Contact Model

```json
{
  "id": "integer",
  "first_name": "string",
  "last_name": "string",
  "company": "string",
  "telephone": "string",
  "email": "string",
  "address": "string",
  "notes": "string"
}
```

## Contact

Project Link: [https://github.com/ataagri/cs436-term-project](https://github.com/ataagri/cs436-term-project)

---

Built with ❤️ using React, FastAPI, and Google Cloud Platform.
## Troubleshooting

### Common Issues and Solutions

#### Docker Setup Issues

1. **Port conflicts**:
   - Error: `port is already allocated`
   - Solution: Check if another application is using the required ports (3000, 8000, 5432, 9090, 3001). Stop those applications or change the ports in `docker-compose.yml`.

2. **Docker permission issues**:
   - Error: `permission denied` when running Docker commands
   - Solution: Add your user to the Docker group: `sudo usermod -aG docker $USER` and then log out and back in.

3. **Docker Compose not found**:
   - Error: `docker-compose: command not found`
   - Solution: Install Docker Compose separately or use the plugin version with `docker compose` (note the space instead of hyphen).

#### Database Connection Issues

1. **Cannot connect to PostgreSQL**:
   - Error: `could not connect to server: Connection refused`
   - Solution: Ensure PostgreSQL is running and check the connection parameters (host, port, username, password).

2. **Cloud SQL Proxy connection issues**:
   - Error: `failed to connect to instance`
   - Solution: Verify your GCP credentials, project ID, and instance name. Ensure you have the necessary permissions.

#### Frontend Issues

1. **Firebase configuration errors**:
   - Error: `Firebase App named '[DEFAULT]' already exists`
   - Solution: Ensure you're not initializing Firebase multiple times in your code.

2. **API connection errors**:
   - Error: `Network Error` when calling the API
   - Solution: Check that the backend is running and that `REACT_APP_API_URL` is set correctly in your `.env.local` file.

3. **Authentication issues**:
   - Error: `auth/invalid-api-key` or similar Firebase auth errors
   - Solution: Verify your Firebase configuration in `.env.local` and ensure all required values are set correctly.

#### Backend Issues

1. **Database migration errors**:
   - Error: `sqlalchemy.exc.OperationalError` when running `create_db.py`
   - Solution: Check database connection parameters and ensure the database exists.

2. **Environment variable issues**:
   - Error: Missing environment variables
   - Solution: Ensure all required environment variables are set or use the default values provided in the code.

### Verification Steps

To verify your setup is working correctly:

1. **Database Connection**:
   ```bash
   # Using Docker
   docker exec -it contacts-db psql -U contacts-user -d contacts -c "SELECT 1"
   
   # Using psql client
   psql -h localhost -U contacts-user -d contacts -c "SELECT 1"
   ```

2. **Backend API**:
   ```bash
   curl http://localhost:8000/health
   ```

3. **Frontend Connection to Backend**:
   - Open the browser console in the frontend application
   - Check for network requests to the backend API
   - Verify no CORS or connection errors

4. **Monitoring**:
   - Access Prometheus at http://localhost:9090
   - Go to Status > Targets to verify the backend is being scraped
   - Access Grafana at http://localhost:3001 and verify the Prometheus data source is connected
