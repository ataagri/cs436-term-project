# Containerizing the FastAPI Backend

## 1. Create a Dockerfile

Create a Dockerfile in the backend directory:

```bash
# Create Dockerfile
touch /Users/ataagri/sabanci/cs436/cs436-term-project/backend/Dockerfile
```

Add the following content to the Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install pipenv and dependencies
RUN pip install pipenv && \
    pipenv install --deploy --system && \
    pip uninstall -y pipenv

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 2. Create .dockerignore

Create a .dockerignore file to exclude unnecessary files:

```bash
# Create .dockerignore
touch /Users/ataagri/sabanci/cs436/cs436-term-project/backend/.dockerignore
```

Add the following content to the .dockerignore file:

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
contacts.db
.env
.venv
env/
venv/
ENV/
.idea/
.git/
```

## 3. Build and Push Docker Image

Build the Docker image and push it to Artifact Registry:

```bash
# Navigate to the backend directory
cd /Users/ataagri/sabanci/cs436/cs436-term-project/backend

# Build the Docker image
docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/contacts-repo/backend:v1 .

# Push the image to Artifact Registry
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/contacts-repo/backend:v1
```

Replace `YOUR_PROJECT_ID` with your actual GCP project ID.

## 4. Test the Docker Image Locally

Before pushing to GCP, test the Docker image locally:

```bash
# Run the container locally
docker run -p 8000:8000 \
  -e DB_USER=contacts-user \
  -e DB_PASSWORD=YOUR_USER_PASSWORD \
  -e DB_NAME=contacts \
  -e CLOUD_SQL_PROXY=true \
  us-central1-docker.pkg.dev/YOUR_PROJECT_ID/contacts-repo/backend:v1
```

## 5. Update CORS Configuration

Update the CORS configuration in `main.py` to allow requests from your Firebase Hosting URL:

```python
# Update origins list in main.py
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://YOUR_PROJECT_ID.web.app",
    "https://YOUR_PROJECT_ID.firebaseapp.com",
]
```

## 6. Create Kubernetes Deployment Files

Create a directory for Kubernetes configuration files:

```bash
# Create directory for Kubernetes files
mkdir -p /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes
```

Create a deployment.yaml file:

```bash
# Create deployment.yaml
touch /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/backend-deployment.yaml
```

Add the following content to the deployment.yaml file:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: contacts-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: contacts-backend
  template:
    metadata:
      labels:
        app: contacts-backend
    spec:
      containers:
      - name: contacts-backend
        image: us-central1-docker.pkg.dev/YOUR_PROJECT_ID/contacts-repo/backend:v1
        ports:
        - containerPort: 8000
        env:
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: cloudsql-db-credentials
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: cloudsql-db-credentials
              key: password
        - name: DB_NAME
          value: contacts
        - name: DB_HOST
          value: /cloudsql/YOUR_PROJECT_ID:us-central1:contacts-db
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
      # Cloud SQL Proxy sidecar container
      - name: cloudsql-proxy
        image: gcr.io/cloudsql-docker/gce-proxy:1.31.0
        command:
          - "/cloud_sql_proxy"
          - "-instances=YOUR_PROJECT_ID:us-central1:contacts-db=tcp:5432"
        securityContext:
          runAsNonRoot: true
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
```

Create a service.yaml file:

```bash
# Create service.yaml
touch /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/backend-service.yaml
```

Add the following content to the service.yaml file:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: contacts-backend
spec:
  selector:
    app: contacts-backend
  ports:
  - port: 80
    targetPort: 8000
  type: NodePort
```

Create a secret for database credentials:

```bash
# Create db-credentials.yaml
touch /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/db-credentials.yaml
```

Add the following content to the db-credentials.yaml file:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloudsql-db-credentials
type: Opaque
stringData:
  username: contacts-user
  password: YOUR_USER_PASSWORD
```

Replace `YOUR_PROJECT_ID` and `YOUR_USER_PASSWORD` with your actual values.