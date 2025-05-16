# Google Kubernetes Engine (GKE) Setup

## 1. Create a GKE Cluster

Create a GKE cluster to host the FastAPI backend:

```bash
# Create a GKE cluster
gcloud container clusters create contacts-cluster \
    --num-nodes=3 \
    --zone=us-central1-a \
    --machine-type=e2-standard-2 \
    --release-channel=regular \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=5 \
    --service-account=gke-service-account@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## 2. Get Credentials for the Cluster

Configure kubectl to use the new cluster:

```bash
# Get credentials
gcloud container clusters get-credentials contacts-cluster --zone=us-central1-a
```

## 3. Apply Kubernetes Configuration Files

Apply the Kubernetes configuration files to deploy the application:

```bash
# Apply database credentials secret
kubectl apply -f /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/db-credentials.yaml

# Apply deployment
kubectl apply -f /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/backend-deployment.yaml

# Apply service
kubectl apply -f /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/backend-service.yaml
```

## 4. Create Ingress for External Access

Create an ingress resource to expose the backend through a load balancer:

```bash
# Create ingress.yaml
touch /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/ingress.yaml
```

Add the following content to the ingress.yaml file:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: contacts-ingress
  annotations:
    kubernetes.io/ingress.global-static-ip-name: contacts-ip
    networking.gke.io/managed-certificates: contacts-certificate
    kubernetes.io/ingress.class: "gce"
spec:
  rules:
  - host: api.YOUR_DOMAIN.com  # Replace with your domain
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: contacts-backend
            port:
              number: 80
```

Apply the ingress resource:

```bash
# Apply ingress
kubectl apply -f /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/ingress.yaml
```

## 5. Create a Static IP Address

Reserve a static IP address for the application:

```bash
# Create a static IP address
gcloud compute addresses create contacts-ip --global
```

Get the assigned IP address:

```bash
# Get the IP address
gcloud compute addresses describe contacts-ip --global
```

## 6. Set Up a Domain (Optional)

If you have a domain, configure it to point to the static IP address:

1. Create an A record in your DNS configuration pointing to the static IP address
2. Create a managed certificate in GKE:

```bash
# Create certificate.yaml
touch /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/certificate.yaml
```

Add the following content to the certificate.yaml file:

```yaml
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: contacts-certificate
spec:
  domains:
  - api.YOUR_DOMAIN.com  # Replace with your domain
```

Apply the certificate resource:

```bash
# Apply certificate
kubectl apply -f /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/certificate.yaml
```

## 7. Monitor Deployment

Monitor the deployment to ensure it's running correctly:

```bash
# Check deployments
kubectl get deployments

# Check pods
kubectl get pods

# Check services
kubectl get services

# Check ingress
kubectl get ingress

# View logs for a pod
kubectl logs <pod-name>
```

## 8. Configure Autoscaling

Set up horizontal pod autoscaling for the backend:

```bash
# Create autoscale.yaml
touch /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/autoscale.yaml
```

Add the following content to the autoscale.yaml file:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: contacts-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: contacts-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

Apply the autoscaling configuration:

```bash
# Apply autoscaling
kubectl apply -f /Users/ataagri/sabanci/cs436/cs436-term-project/kubernetes/autoscale.yaml
```

Replace `YOUR_PROJECT_ID` and `YOUR_DOMAIN.com` with your actual values.