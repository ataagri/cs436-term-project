### 1. Baseline Test
bash
locust -f locustfile.py --host https://api.ataagri.com --users 50 --spawn-rate 5 --run-time 5m --html=baseline_report.html


### 2. Moderate Load Test
bash
locust -f locustfile.py --host https://api.ataagri.com --users 200 --spawn-rate 10 --run-time 10m --html=moderate_report.html


### 3. High Load Test
bash
locust -f locustfile.py --host https://api.ataagri.com --users 500 --spawn-rate 20 --run-time 15m --html=high_report.html


### 4. Very High Load Test
bash
locust -f locustfile.py --host https://api.ataagri.com --users 1000 --spawn-rate 30 --run-time 20m --html=very_high_report.html