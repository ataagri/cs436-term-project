# Load Testing with Locust for ReactFast Contacts

This directory contains Locust test scripts and configurations for load testing the ReactFast Contacts application deployed on Google Cloud Platform.

## Prerequisites

- Python 3.7+
- Locust (`pip install locust`)
- Access to the deployed API (https://api.ataagri.com)

## Test Files

- `locustfile.py`: The main Locust test script defining user behaviors
- `config.yaml`: Configuration file for Locust
- `run_test.sh`: Shell script to run a series of tests with different parameters

## Running Tests

### Option 1: Using the Web UI

1. Navigate to the testing directory:
   ```bash
   cd testing
   ```

2. Start Locust:
   ```bash
   locust -f locustfile.py --host https://api.ataagri.com
   ```

3. Open your browser and go to http://localhost:8089
4. Enter the number of users, spawn rate, and start the test

### Option 2: Using the Configuration File

```bash
locust --config config.yaml
```

### Option 3: Using the Automated Test Script

```bash
chmod +x run_test.sh
./run_test.sh
```

## Test Scenarios

The test script includes several user behaviors with different frequencies:

- **Get All Contacts (30%)**: Simulates retrieving the full contact list
- **Get Single Contact (20%)**: Simulates retrieving a specific contact
- **Create Contact (10%)**: Simulates adding a new contact
- **Update Contact (10%)**: Simulates updating an existing contact
- **Delete Contact (5%)**: Simulates deleting a contact
- **Health Check (2%)**: Occasionally checks the API health endpoint
- **Metrics Check**: A separate user class that checks the Prometheus metrics endpoint

## Interpreting Results

After running tests, Locust provides several metrics:

- **Request Count**: Total number of requests made
- **Response Time**: Min, max, average, and median response times
- **Requests Per Second**: The throughput of your application
- **Failure Rate**: Percentage of failed requests

## Observing Kubernetes Scaling

While the tests are running, you can observe how your Kubernetes pods scale:

```bash
# Get the current number of pods
kubectl get pods -n default

# Watch the pods scale in real-time
kubectl get pods -n default -w

# Check the HPA (Horizontal Pod Autoscaler) status
kubectl get hpa
```

## Visualizing Results

### Locust Web UI

The Locust web interface provides real-time charts and statistics during test execution.

### Grafana Dashboards

Access your Grafana instance (likely on your monitoring VM) to observe:

1. **API Performance**: Request rates, response times, error rates
2. **Kubernetes Metrics**: Pod count, CPU/memory usage, scaling events
3. **Database Performance**: Query rates, connection counts, etc.

Typical Grafana URL: http://[YOUR-MONITORING-VM-IP]:3001

### Prometheus Queries

Some useful Prometheus queries to create custom visualizations:

- Pod count: `count(kube_pod_info{namespace="default", pod=~"contacts-backend.*"})`
- API request rate: `sum(rate(http_requests_total{handler="/contacts"}[1m]))`
- Response time: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))`
- CPU usage: `sum(rate(container_cpu_usage_seconds_total{namespace="default", pod=~"contacts-backend.*"}[1m]))`

## Exporting Results

Locust can export test results in various formats:

- **CSV**: `locust -f locustfile.py --csv=results`
- **HTML**: `locust -f locustfile.py --html=report.html`

The `run_test.sh` script automatically saves results in both formats.
