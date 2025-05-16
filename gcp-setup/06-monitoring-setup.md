# Monitoring Dashboard Setup with VM

## 1. Create a Virtual Machine Instance

Create a Compute Engine VM instance for the monitoring dashboard:

```bash
# Create a VM instance
gcloud compute instances create monitoring-dashboard \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --subnet=default \
    --tags=http-server,https-server \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --boot-disk-size=20GB \
    --boot-disk-type=pd-balanced \
    --boot-disk-device-name=monitoring-dashboard
```

## 2. Set Up Firewall Rules

Create firewall rules to allow HTTP and HTTPS traffic:

```bash
# Create firewall rule for HTTP
gcloud compute firewall-rules create allow-http \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:80 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server

# Create firewall rule for HTTPS
gcloud compute firewall-rules create allow-https \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:443 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=https-server
```

## 3. Connect to the VM

SSH into the VM:

```bash
# SSH into the VM
gcloud compute ssh monitoring-dashboard --zone=us-central1-a
```

## 4. Install Required Software

Install the necessary software on the VM:

```bash
# Update package lists
sudo apt-get update

# Install dependencies
sudo apt-get install -y build-essential nginx certbot python3-certbot-nginx python3-pip git

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install npm global packages
sudo npm install -g pm2
```

## 5. Set Up Prometheus and Grafana

Create a Docker Compose configuration for Prometheus and Grafana:

```bash
# Create a directory for the monitoring stack
mkdir -p ~/monitoring
cd ~/monitoring

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"
    networks:
      - monitoring
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=password
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3000:3000"
    networks:
      - monitoring
    restart: unless-stopped

networks:
  monitoring:
    driver: bridge

volumes:
  prometheus_data:
  grafana_data:
EOF

# Create Prometheus configuration directory
mkdir -p prometheus

# Create prometheus.yml configuration file
cat > prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "gke"
    kubernetes_sd_configs:
      - role: pod
        api_server: https://kubernetes.default.svc
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name
EOF

# Create directory for Grafana provisioning
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards

# Create Grafana datasource configuration
cat > grafana/provisioning/datasources/datasource.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    access: proxy
    isDefault: true
EOF

# Create Grafana dashboard configuration
cat > grafana/provisioning/dashboards/dashboard.yml << 'EOF'
apiVersion: 1

providers:
  - name: 'Default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /var/lib/grafana/dashboards
EOF

# Create directory for Grafana dashboards
mkdir -p grafana/dashboards

# Start the containers
sudo docker-compose up -d
```

## 6. Install and Configure Node Exporter on the Backend VMs

For GKE nodes, create a DaemonSet to run node-exporter:

```bash
# Create node-exporter.yaml
mkdir -p ~/kubernetes
cat > ~/kubernetes/node-exporter.yaml << 'EOF'
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: default
  labels:
    k8s-app: node-exporter
spec:
  selector:
    matchLabels:
      k8s-app: node-exporter
  template:
    metadata:
      labels:
        k8s-app: node-exporter
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9100"
    spec:
      containers:
      - name: node-exporter
        image: prom/node-exporter:latest
        ports:
        - containerPort: 9100
          protocol: TCP
          name: http
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
          requests:
            cpu: 10m
            memory: 100Mi
        securityContext:
          privileged: true
        volumeMounts:
        - name: proc
          mountPath: /host/proc
          readOnly: true
        - name: sys
          mountPath: /host/sys
          readOnly: true
        - name: root
          mountPath: /rootfs
          readOnly: true
      hostNetwork: true
      hostPID: true
      volumes:
      - name: proc
        hostPath:
          path: /proc
      - name: sys
        hostPath:
          path: /sys
      - name: root
        hostPath:
          path: /
EOF

# Apply the DaemonSet
kubectl apply -f ~/kubernetes/node-exporter.yaml
```

## 7. Create a Service for Node Exporter

Create a Kubernetes Service to expose node-exporter:

```bash
# Create node-exporter-service.yaml
cat > ~/kubernetes/node-exporter-service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: node-exporter
  namespace: default
  labels:
    k8s-app: node-exporter
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9100"
spec:
  ports:
  - port: 9100
    targetPort: 9100
    protocol: TCP
    name: http
  selector:
    k8s-app: node-exporter
EOF

# Apply the Service
kubectl apply -f ~/kubernetes/node-exporter-service.yaml
```

## 8. Setup Monitoring for Cloud SQL

Integrate Cloud SQL monitoring with Prometheus using Cloud SQL Proxy:

```bash
# Create a VM monitoring proxy for Cloud SQL
# (In practice, you would use another method to securely receive metrics from Cloud SQL)
gcloud compute instances create sql-monitoring-proxy \
    --zone=us-central1-a \
    --machine-type=e2-small \
    --subnet=default \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --boot-disk-size=10GB
```

SSH into the sql-monitoring-proxy VM:

```bash
# SSH into the VM
gcloud compute ssh sql-monitoring-proxy --zone=us-central1-a
```

Set up a Cloud SQL exporter on the proxy VM:

```bash
# Install Docker and prerequisites
sudo apt-get update
sudo apt-get install -y docker.io

# Run a Postgres exporter container
sudo docker run -d \
  --name postgres_exporter \
  -p 9187:9187 \
  -e DATA_SOURCE_NAME="postgresql://contacts-user:YOUR_USER_PASSWORD@localhost:5432/contacts?host=/cloudsql/YOUR_PROJECT_ID:us-central1:contacts-db" \
  -v /path/to/service-account-key.json:/secrets/service-account-key.json \
  quay.io/prometheuscommunity/postgres-exporter
```

## 9. Create Custom Dashboards in Grafana

Access Grafana at http://MONITORING_VM_IP:3000 and set up dashboards:

1. Log in with the default credentials (admin/password)
2. Navigate to "Dashboards" > "Create" > "New Dashboard"
3. Add the following panels:

### 9.1. GKE Node Resource Usage
- Create a panel to monitor CPU and memory usage of GKE nodes
- Use queries like `node_cpu_seconds_total` and `node_memory_MemTotal_bytes - node_memory_MemFree_bytes`

### 9.2. FastAPI Pod Metrics
- Create a panel to monitor FastAPI pods resource usage and requests
- Use queries for pod CPU, memory, and HTTP request metrics

### 9.3. Cloud SQL Metrics
- Create a panel to monitor Cloud SQL database metrics
- Use Postgres exporter metrics like `pg_stat_database_tup_fetched` and `pg_stat_database_tup_inserted`

### 9.4. Firebase Metrics
- Integrate Firebase performance metrics using custom exporters

## 10. Set Up Nginx as a Reverse Proxy

Configure Nginx to serve the dashboard securely:

```bash
# Create Nginx configuration
sudo cat > /etc/nginx/sites-available/monitoring << 'EOF'
server {
    listen 80;
    server_name monitoring.YOUR_DOMAIN.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /prometheus {
        proxy_pass http://localhost:9090;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/monitoring /etc/nginx/sites-enabled/

# Remove the default site
sudo rm /etc/nginx/sites-enabled/default

# Test the configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## 11. Set Up SSL with Let's Encrypt

Secure the dashboard with an SSL certificate:

```bash
# Get an SSL certificate
sudo certbot --nginx -d monitoring.YOUR_DOMAIN.com

# Follow the interactive prompts
```

## 12. Set Up Alerting

Configure Grafana alerts to notify when issues are detected:

1. In Grafana, go to "Alerting" > "Notification channels"
2. Add channels for email, Slack, or other notification methods
3. Create alert rules in your dashboards to trigger notifications

Replace `YOUR_PROJECT_ID`, `YOUR_USER_PASSWORD`, and `YOUR_DOMAIN.com` with your actual values.