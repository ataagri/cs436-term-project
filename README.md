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
  - [Frontend Setup](#frontend-setup)
  - [Backend Setup](#backend-setup)
  - [Database Setup](#database-setup)
  - [Local Development](#local-development)
- [Google Cloud Deployment](#google-cloud-deployment)
- [API Documentation](#api-documentation)
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
- **Local Development**: Easy setup for local development
- **Containerization**: Docker support for consistent environments
- **Detailed Documentation**: Comprehensive setup and deployment guides

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
└── kubernetes/               # Kubernetes configuration files
    ├── backend-deployment-latest.yaml # Backend deployment configuration
    ├── backend-service.yaml  # Backend service configuration
    ├── ingress.yaml          # Ingress configuration
    ├── certificate.yaml      # SSL certificate configuration
    ├── db-credentials.yaml   # Database credentials configuration
    └── autoscale.yaml        # HPA configuration
```

## Setup and Installation

### Prerequisites

- Node.js (v14 or later)
- Python (v3.8 or later)
- Docker and Docker Compose
- Google Cloud SDK
- kubectl
- Firebase CLI

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file with your API URL:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm start
   ```

5. The application will be available at `http://localhost:3000`

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies using Pipenv:
   ```bash
   pipenv install
   ```

3. Set up environment variables for local development:
   ```bash
   export DB_USER=your_db_user
   export DB_PASSWORD=your_db_password
   export DB_NAME=contacts
   export DB_HOST=localhost
   export DB_PORT=5432
   export CLOUD_SQL_PROXY=true
   ```

4. Start the development server:
   ```bash
   pipenv run uvicorn main:app --reload
   ```

5. The API will be available at `http://localhost:8000`

### Database Setup

1. Set up a local PostgreSQL database:
   ```bash
   docker run --name contacts-db -e POSTGRES_PASSWORD=your_password -e POSTGRES_USER=your_user -e POSTGRES_DB=contacts -p 5432:5432 -d postgres:13
   ```

2. Initialize the database:
   ```bash
   cd backend
   pipenv run python create_db.py
   ```

### Local Development

For local development with a full environment:

1. Run the React frontend:
   ```bash
   cd frontend
   npm start
   ```

2. Run the FastAPI backend with Cloud SQL Proxy (for local development with GCP):
   ```bash
   cd backend
   CLOUD_SQL_PROXY=true pipenv run uvicorn main:app --reload
   ```

3. Or run with a local PostgreSQL database:
   ```bash
   cd backend
   pipenv run uvicorn main:app --reload
   ```

## Google Cloud Deployment

The application is designed to be deployed to Google Cloud Platform using a production-ready architecture. The deployment process involves several key steps:

### GCP Project and Infrastructure Setup

1. Create a new GCP project and enable required APIs:
   - Compute Engine API
   - Kubernetes Engine API
   - Cloud SQL Admin API
   - Cloud Build API
   - Container Registry API
   - Firebase API

2. Set up Firebase project:
   - Create a new Firebase project linked to your GCP project
   - Enable Authentication with Email/Password provider
   - Configure Firebase Hosting

3. Configure service accounts with appropriate permissions:
   - Cloud SQL Client
   - Kubernetes Engine Admin
   - Storage Admin

### Database Deployment

1. Create a PostgreSQL instance on Cloud SQL:
   ```bash
   gcloud sql instances create contacts-db \
     --database-version=POSTGRES_13 \
     --tier=db-f1-micro \
     --region=us-central1 \
     --storage-type=SSD \
     --storage-size=10GB \
     --root-password=[PASSWORD]
   ```

2. Create database and user:
   ```bash
   gcloud sql databases create contacts --instance=contacts-db
   gcloud sql users create contacts-user --instance=contacts-db --password=[PASSWORD]
   ```

3. Set up Cloud SQL Proxy for secure connections.

### Backend Deployment

1. Build and push the Docker image:
   ```bash
   cd backend
   docker build -t gcr.io/[PROJECT_ID]/contacts-backend:latest .
   docker push gcr.io/[PROJECT_ID]/contacts-backend:latest
   ```

2. Create a GKE cluster:
   ```bash
   gcloud container clusters create contacts-cluster \
     --zone us-central1-a \
     --num-nodes 3 \
     --machine-type e2-standard-2
   ```

3. Deploy to Kubernetes using the configuration files in the `kubernetes` directory:
   ```bash
   kubectl apply -f kubernetes/db-credentials.yaml
   kubectl apply -f kubernetes/backend-deployment-latest.yaml
   kubectl apply -f kubernetes/backend-service.yaml
   kubectl apply -f kubernetes/certificate.yaml
   kubectl apply -f kubernetes/ingress.yaml
   kubectl apply -f kubernetes/autoscale.yaml
   ```

### Frontend Deployment

1. Configure Firebase in the frontend:
   - Update the Firebase configuration in `frontend/src/firebase.js`
   - Set the correct API URL in `.env.production`

2. Deploy to Firebase Hosting:
   ```bash
   cd frontend
   npm run build
   firebase deploy --only hosting
   ```

### Cloud Functions Deployment

1. Deploy Firebase Cloud Functions:
   ```bash
   cd functions
   npm install
   firebase deploy --only functions
   ```

### Monitoring Setup

1. Set up Prometheus and Grafana on a Compute Engine VM for monitoring
2. Configure exporters to collect metrics from GKE and Cloud SQL
3. Create dashboards to monitor application performance and resource usage

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