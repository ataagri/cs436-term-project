"""API for contact database"""
from typing import List, Optional
import logging

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import the Prometheus instrumentator
from prometheus_fastapi_instrumentator import Instrumentator

import models
from db import SessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# allows cross-origin requests from any origin for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to log requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request information"""
    logger.info(f"Request path: {request.url.path}")
    logger.info(f"Client: {request.client}")
    logger.info(f"Headers: {request.headers}")
    
    response = await call_next(request)
    return response

class Contact(BaseModel):
    """Contact model"""

    id: Optional[int] = None
    first_name: str
    last_name: str
    company: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        """Pydantic config"""
        orm_mode = True

def get_db():
    """creates separate sessions for each request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    """Root endpoint for health check"""
    return {"status": "OK", "message": "Contact API is running"}

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is operational"}

@app.get("/contacts", response_model=List[Contact], status_code=status.HTTP_200_OK)
def get_all_contacts(db: Session = Depends(get_db)):
    """READ: Get all contacts"""
    logger.info("Getting all contacts")
    try:
        contacts = db.query(models.Contact).all()
        logger.info(f"Retrieved {len(contacts)} contacts")
        return contacts
    except Exception as e:
        logger.error(f"Error retrieving contacts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
        )

@app.get(
    "/contacts/{contact_id}", response_model=Contact, status_code=status.HTTP_200_OK
)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """READ: Get a contact by id"""
    logger.info(f"Getting contact with id: {contact_id}")
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact

@app.post(
    "/contacts", response_model=Contact, status_code=status.HTTP_201_CREATED
)
def create_contact(contact: Contact, db: Session = Depends(get_db)):
    """CREATE: Create a new contact"""
    logger.info(f"Creating contact: {contact.first_name} {contact.last_name}")
    
    # Fixed the logical condition - was using 'and' incorrectly
    db_contact = db.query(models.Contact).filter(
        (models.Contact.first_name == contact.first_name) & 
        (models.Contact.last_name == contact.last_name) &
        (models.Contact.email == contact.email)
    ).first()

    if db_contact is not None:
        logger.warning(f"Contact already exists: {contact.first_name} {contact.last_name}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="🤨 Contact already exists"
        )

    new_contact = models.Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        company=contact.company,
        telephone=contact.telephone,
        email=contact.email,
        address=contact.address,
        notes=contact.notes,
    )

    try:
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        logger.info(f"Contact created with id: {new_contact.id}")
        return new_contact
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
        )

@app.patch(
    "/contacts/{contact_id}",
    response_model=Contact,
    status_code=status.HTTP_200_OK,
)
def update_contact(contact_id: int, contact: Contact, db: Session = Depends(get_db)):
    """UPDATE: Update a contact"""
    logger.info(f"Updating contact with id: {contact_id}")
    contact_to_update = (
        db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    )
    
    if contact_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    contact_to_update.first_name = contact.first_name
    contact_to_update.last_name = contact.last_name
    contact_to_update.company = contact.company
    contact_to_update.telephone = contact.telephone
    contact_to_update.email = contact.email
    contact_to_update.address = contact.address
    contact_to_update.notes = contact.notes

    try:
        db.commit()
        logger.info(f"Contact updated: {contact_id}")
        return contact_to_update
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating contact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
        )

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """DELETE: Delete a contact"""
    logger.info(f"Deleting contact with id: {contact_id}")
    contact_to_delete = (
        db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    )

    if contact_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="✋ Contact does not exist"
        )

    try:
        db.delete(contact_to_delete)
        db.commit()
        logger.info(f"Contact deleted: {contact_id}")
        return {"message": "👌 Contact deleted"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting contact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
        )
