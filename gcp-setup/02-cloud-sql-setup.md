# Cloud SQL PostgreSQL Setup

## 1. Create PostgreSQL Instance

Create a PostgreSQL instance in Cloud SQL:

```bash
# Create a PostgreSQL instance
gcloud sql instances create contacts-db \
    --database-version=POSTGRES_13 \
    --cpu=1 \
    --memory=3840MB \
    --region=us-central1 \
    --root-password=YOUR_ROOT_PASSWORD
```

## 2. Create Database and User

Create a database and user for the application:

```bash
# Create a database
gcloud sql databases create contacts \
    --instance=contacts-db

# Create a user
gcloud sql users create contacts-user \
    --instance=contacts-db \
    --password=YOUR_USER_PASSWORD
```

## 3. Configure Connection

After creating the database, you'll need the connection information:

- Instance Connection Name: `YOUR_PROJECT_ID:us-central1:contacts-db`
- Database Name: `contacts`
- Username: `contacts-user`
- Password: `YOUR_USER_PASSWORD`

## 4. Configure SSL (Optional but Recommended)

For secure connections to your Cloud SQL instance:

```bash
# For SSL connections, a simpler alternative is to use the Cloud SQL Auth Proxy
# which handles SSL encryption automatically without requiring certificate management

# 1. Download the proxy (see "Cloud SQL Proxy for Local Development" section below)

# 2. Start the proxy with:
./cloud-sql-proxy --instances=YOUR_PROJECT_ID:us-central1:contacts-db=tcp:5432

# 3. Connect to your database using standard PostgreSQL tools, but connect to localhost:5432

# Note: If you still need to set up manual SSL certificates, follow Google Cloud's
# latest documentation at: https://cloud.google.com/sql/docs/postgres/configure-ssl-instance
```

## 5. Modify Backend Database Configuration

Update the backend configuration to use PostgreSQL:

1. Create a secrets file for database credentials
2. Update the db.py file to use PostgreSQL instead of SQLite

Example modification for `db.py`:

```python
""" database set up"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL connection string
DB_USER = os.environ.get("DB_USER", "contacts-user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "YOUR_USER_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "/cloudsql/YOUR_PROJECT_ID:us-central1:contacts-db")
DB_NAME = os.environ.get("DB_NAME", "contacts")

# For local development with Cloud SQL proxy
CLOUD_SQL_PROXY = os.environ.get("CLOUD_SQL_PROXY", False)
if CLOUD_SQL_PROXY:
    POSTGRES_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@127.0.0.1:5432/{DB_NAME}"
else:
    # For production deployment
    POSTGRES_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(POSTGRES_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# declarative base class
Base = declarative_base()
```

## 6. Cloud SQL Proxy for Local Development

To connect to your Cloud SQL instance locally:

1. Install the Cloud SQL Proxy:
   ```bash
   # Download the proxy
   curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.6.0/cloud-sql-proxy.darwin.amd64 // For amd64
   curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.6.0/cloud-sql-proxy.darwin.arm64 // For arm64 (Apple Silicon)
   
   # Make the proxy executable
   chmod +x cloud-sql-proxy
   ```

2. Start the proxy:
   ```bash
   # Run the Cloud SQL Proxy
   ./cloud-sql-proxy cs436-reactfastcontacts:us-central1:contacts-db --port=5432
   ```

3. Run your application with the `CLOUD_SQL_PROXY` environment variable set:
   ```bash
   # Run the application
   CLOUD_SQL_PROXY=true uvicorn main:app --reload
   ```

## 7. Migrate Data to PostgreSQL

Run the updated `create_db.py` script to create tables and insert initial data:

```bash
# Run with Cloud SQL Proxy (local development)
CLOUD_SQL_PROXY=true python create_db.py

# Or when deployed to GKE, the script will use the production connection
```