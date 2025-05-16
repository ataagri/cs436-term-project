""" database set up"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL connection string
DB_USER = os.environ.get("DB_USER", "contacts-user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "AtaIdilSarp123")
DB_HOST = os.environ.get("DB_HOST", "/cloudsql/cs436-reactfastcontacts:us-central1:contacts-db")
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