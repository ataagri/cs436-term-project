#!/bin/bash
# Start cloud-sql-proxy and the backend application

# Check if cloud-sql-proxy is in PATH
if [ ! -f ../cloud-sql-proxy ]; then
    echo "Cloud SQL Proxy not found. Please download it first."
    exit 1
fi

# Start cloud-sql-proxy in background
echo "Starting Cloud SQL Proxy..."
../cloud-sql-proxy cs436-reactfastcontacts:us-central1:contacts-db --port=5432 &
PROXY_PID=$!

# Wait for proxy to start
sleep 3

# Set environment variables
export CLOUD_SQL_PROXY=true
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=contacts-user
export DB_PASSWORD=AtaIdilSarp123
export DB_NAME=contacts

# Create database tables if needed
echo "Creating database tables..."
python create_db.py

# Start FastAPI application
echo "Starting FastAPI application..."
pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Cleanup on exit
function cleanup {
    echo "Shutting down Cloud SQL Proxy..."
    kill $PROXY_PID
}

trap cleanup EXIT