# Testing and Troubleshooting

## 1. Testing the Complete Application Flow

### 1.1. Test Firebase Authentication

Test the authentication flow in the frontend application:

1. Open the deployed frontend application (https://YOUR_PROJECT_ID.web.app)
2. Try to sign up with a new account
3. Verify that the account is created in Firebase Authentication console
4. Try to sign in with the created account
5. Verify that the authentication token is being passed to the backend

### 1.2. Test GKE Backend

Test the backend API running on GKE:

```bash
# Get the external IP address of the ingress
kubectl get ingress contacts-ingress

# Test the API endpoints
curl -X GET https://api.YOUR_DOMAIN.com/all-contacts
```

If using authentication:

```bash
# Get an authentication token (using Firebase Admin SDK or client SDK)
TOKEN="your_auth_token"

# Test the API endpoints with authentication
curl -X GET https://api.YOUR_DOMAIN.com/all-contacts \
  -H "Authorization: Bearer $TOKEN"
```

### 1.3. Test Database Connectivity

Test the connection to Cloud SQL from the backend:

```bash
# Get a pod name
POD_NAME=$(kubectl get pods -l app=contacts-backend -o jsonpath="{.items[0].metadata.name}")

# Execute a command to test database connectivity
kubectl exec -it $POD_NAME -- python -c "from db import engine; print('Database connection successful:', engine.connect())"
```

### 1.4. Test End-to-End Flow

Test the complete flow from frontend to backend to database:

1. Sign in to the frontend application
2. Create a new contact
3. Verify that the contact is displayed in the contacts list
4. Edit the contact information
5. Verify that the changes are saved
6. Delete the contact
7. Verify that the contact is removed from the list

## 2. Common Troubleshooting

### 2.1. Backend Service Issues

If the backend service is not accessible:

```bash
# Check if pods are running
kubectl get pods -l app=contacts-backend

# Check pod logs
kubectl logs -l app=contacts-backend

# Check deployment status
kubectl describe deployment contacts-backend

# Check service status
kubectl describe service contacts-backend

# Check ingress status
kubectl describe ingress contacts-ingress
```

### 2.2. Database Connection Issues

If there are issues connecting to the database:

```bash
# Check Cloud SQL logs
gcloud logging read "resource.type=cloudsql_database AND resource.labels.database_id=YOUR_PROJECT_ID:us-central1:contacts-db"

# Check Cloud SQL Proxy logs in the pod
POD_NAME=$(kubectl get pods -l app=contacts-backend -o jsonpath="{.items[0].metadata.name}")
kubectl logs $POD_NAME -c cloudsql-proxy

# Test database connectivity from the pod
kubectl exec -it $POD_NAME -- python -c "import psycopg2; conn = psycopg2.connect(host='127.0.0.1', port=5432, dbname='contacts', user='contacts-user', password='YOUR_USER_PASSWORD'); print('Connected:', conn.closed == 0)"
```

### 2.3. Firebase Authentication Issues

If there are issues with Firebase Authentication:

1. Check Firebase Authentication logs in the Firebase Console
2. Verify that the Firebase configuration is correct in the frontend
3. Check browser console for any authentication errors
4. Test authentication with Firebase Auth REST API:

```bash
# Get an authentication token
curl -X POST "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary '{"email":"test@example.com","password":"password","returnSecureToken":true}'
```

### 2.4. Networking Issues

If there are networking issues between components:

```bash
# Check GKE network policies
kubectl get networkpolicies

# Test connectivity from a pod to Cloud SQL
POD_NAME=$(kubectl get pods -l app=contacts-backend -o jsonpath="{.items[0].metadata.name}")
kubectl exec -it $POD_NAME -- nc -zv 127.0.0.1 5432

# Test connectivity from a pod to Firebase
kubectl exec -it $POD_NAME -- curl -v https://YOUR_PROJECT_ID.firebaseio.com
```

### 2.5. Monitoring Issues

If there are issues with the monitoring dashboard:

```bash
# Check if Prometheus and Grafana containers are running
sudo docker ps | grep -E "prometheus|grafana"

# Check Prometheus logs
sudo docker logs prometheus

# Check Grafana logs
sudo docker logs grafana

# Check Nginx configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

## 3. Performance Testing

### 3.1. Load Testing the Backend

Use tools like Apache Benchmark (ab) or Locust to test the performance of the backend:

```bash
# Install Apache Benchmark
sudo apt-get install apache2-utils

# Run a load test
ab -n 1000 -c 50 https://api.YOUR_DOMAIN.com/all-contacts
```

### 3.2. Monitoring Performance Metrics

Monitor performance metrics during load testing:

1. Open the Grafana dashboard at http://monitoring.YOUR_DOMAIN.com
2. Watch for changes in CPU, memory, and network usage
3. Check database query performance
4. Identify bottlenecks in the system

### 3.3. Optimizing Performance

Make adjustments based on performance test results:

- Adjust GKE pod resources (CPU and memory)
- Configure autoscaling based on observed metrics
- Optimize database queries
- Implement caching if needed

## 4. Security Testing

### 4.1. Check API Security

Test the security of the API:

```bash
# Test without authentication
curl -X GET https://api.YOUR_DOMAIN.com/all-contacts

# Test with invalid authentication
curl -X GET https://api.YOUR_DOMAIN.com/all-contacts \
  -H "Authorization: Bearer invalid_token"
```

### 4.2. Check Firebase Security Rules

Test Firebase security rules:

1. Open the Firebase Console
2. Go to "Authentication" > "Users"
3. Verify that user data is protected
4. Test access control in your application

### 4.3. Check GKE Security

Review GKE security settings:

```bash
# Check pod security policies
kubectl get podsecuritypolicies

# Check RBAC settings
kubectl get roles
kubectl get rolebindings
kubectl get clusterroles
kubectl get clusterrolebindings
```

## 5. Backup and Recovery

### 5.1. Cloud SQL Backups

Set up automated backups for Cloud SQL:

```bash
# Configure automated backups
gcloud sql instances patch contacts-db \
    --backup-start-time=23:00 \
    --enable-bin-log
```

### 5.2. Test Backup and Recovery

Test the backup and recovery process:

1. Create a manual backup:
   ```bash
   gcloud sql backups create --instance=contacts-db
   ```

2. List available backups:
   ```bash
   gcloud sql backups list --instance=contacts-db
   ```

3. Simulate a recovery:
   ```bash
   # Create a temporary instance for testing restore
   gcloud sql instances create contacts-db-restore \
       --database-version=POSTGRES_13 \
       --cpu=1 \
       --memory=3840MB \
       --region=us-central1 \
       --root-password=YOUR_ROOT_PASSWORD \
       --restore-backup-name=BACKUP_ID \
       --backup-instance=contacts-db
   ```

Replace `YOUR_PROJECT_ID`, `YOUR_USER_PASSWORD`, `YOUR_DOMAIN.com`, `YOUR_API_KEY`, and `BACKUP_ID` with your actual values.