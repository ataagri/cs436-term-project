""" database set up"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL connection string
DB_USER = os.environ.get("DB_USER", "contacts-user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "localpassword")
DB_NAME = os.environ.get("DB_NAME", "contacts")

# For local development with Cloud SQL proxy
CLOUD_SQL_PROXY = os.environ.get("CLOUD_SQL_PROXY", "False").lower() in ("true", "1", "t")
if CLOUD_SQL_PROXY:
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    POSTGRES_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"Using local proxy connection: {POSTGRES_URL}")
else:
    # For production deployment with Cloud SQL Unix socket
    DB_HOST = os.environ.get("DB_HOST", "/cloudsql/cs436-reactfastcontacts:us-central1:contacts-db")
    POSTGRES_URL = f"postgresql:///{DB_NAME}?user={DB_USER}&password={DB_PASSWORD}&host={DB_HOST}"
    print(f"Using Unix socket connection with host: {DB_HOST}")

engine = create_engine(POSTGRES_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# declarative base class
Base = declarative_base()