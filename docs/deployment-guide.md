# Deployment Guide

This guide outlines steps to fix current deployment issues and implement recommended improvements.

## 1. Fix Backend Docker Image Architecture Mismatch

The primary issue is that the backend Docker image was built on ARM64 architecture (likely from an M1/M2 Mac) but GKE clusters run on AMD64 architecture. This mismatch causes the container to crash.

### Solution:

1. Use the platform-specific build script:
   ```bash
   cd backend
   ./build_and_push.sh
   ```

   This script builds a Docker image targeting AMD64 architecture and pushes it to Google Container Registry.

2. Update the Kubernetes deployment:
   ```bash
   cd kubernetes
   ./update-deployment.sh
   ```

   This script:
   - Verifies the image exists
   - Applies the new AMD64-specific deployment
   - Scales down the old deployment
   - Gives you the option to delete the old deployment

## 2. Update Ingress Configuration for Better Security

The current Ingress configuration works but can be improved for production use.

### Domain and DNS Configuration:

1. Set up DNS records for `api.cs436-reactfastcontacts.com` pointing to the static IP `34.36.111.197`
2. Verify that the ManagedCertificate resource is correctly configured (already done)

The certificate may take up to 60 minutes to provision fully. You can check the status with:
```bash
kubectl describe managedcertificate contacts-certificate
```

## 3. Implement Firebase Authentication

To secure your API with Firebase authentication:

1. Add Firebase Admin SDK to backend:
   ```bash
   cd backend
   pipenv install firebase-admin
   ```

2. Create auth.py for token verification (refer to implementation document for details)

3. Modify the backend code to use authentication middleware

4. Update the frontend API calls to include authentication tokens

## 4. Set Up Monitoring

To improve visibility into issues:

1. Enable Cloud Monitoring for your GKE cluster:
   ```bash
   gcloud container clusters update contacts-cluster --monitoring=SYSTEM
   ```

2. Create alerting policies for critical metrics:
   ```bash
   gcloud alpha monitoring policies create --policy-from-file=monitoring/alert-policies.yaml
   ```

3. Set up logging filters for application errors

## 5. Performance Tuning

After fixing the immediate issues, consider these performance improvements:

1. Implement horizontal pod autoscaling:
   ```bash
   kubectl apply -f kubernetes/autoscale.yaml
   ```

2. Add request rate limiting to the Ingress:
   ```yaml
   metadata:
     annotations:
       networking.gke.io/v1beta1.FrontendConfig: "contacts-rate-limit"
   ```

3. Configure Cloud CDN for static assets in Firebase

## Verification Steps

After implementing these changes, verify that:

1. All backend pods are running: 
   ```bash
   kubectl get pods
   ```

2. The application is accessible via the configured domain:
   ```bash
   curl -I https://api.cs436-reactfastcontacts.com/health
   ```

3. The SSL certificate is provisioned:
   ```bash
   kubectl describe managedcertificate contacts-certificate
   ```

4. Authentication is working as expected