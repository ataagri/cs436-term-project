import time
import json
import random
import requests
from locust import HttpUser, task, between, events

# Disable PATCH operations completely since they're causing persistent issues
ENABLE_PATCH = False

class ContactUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Each user instance will maintain its own list of successfully created contacts
        self.my_created_contacts = []
    
    @task(3)
    def get_all_contacts(self):
        """Simulate retrieving all contacts - most common operation"""
        response = self.client.get("/contacts")
        if response.status_code == 200:
            try:
                # Update our list of contact IDs
                contacts = response.json()
                contact_ids = [contact["id"] for contact in contacts]
                
                # Update this user's created contacts list to remove any that no longer exist
                self.my_created_contacts = [cid for cid in self.my_created_contacts if cid in contact_ids]
            except Exception as e:
                print(f"Error updating contact IDs: {e}")
    
    @task(2)
    def get_single_contact(self):
        """Simulate retrieving a single contact"""
        # Prioritize contacts this user created
        if self.my_created_contacts:
            contact_id = random.choice(self.my_created_contacts)
            self.client.get(f"/contacts/{contact_id}")
        else:
            # Get all contacts and pick one randomly
            response = self.client.get("/contacts")
            if response.status_code == 200:
                try:
                    contacts = response.json()
                    if contacts:
                        contact = random.choice(contacts)
                        self.client.get(f"/contacts/{contact['id']}")
                except Exception as e:
                    print(f"Error in get_single_contact: {e}")
    
    @task(2)
    def create_contact(self):
        """Simulate creating a new contact - increased priority since PATCH is disabled"""
        new_contact = {
            "first_name": f"Test{random.randint(1000, 9999)}",
            "last_name": f"User{random.randint(1000, 9999)}",
            "company": "Test Company",
            "telephone": f"+1{random.randint(1000000000, 9999999999)}",
            "email": f"test{random.randint(1000, 9999)}@example.com",
            "address": "123 Test Street",
            "notes": "Created during load testing"
        }
        
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/contacts", json=new_contact, headers=headers)
        
        # If successful, add the new contact ID to our list
        if response.status_code == 201:
            try:
                new_id = response.json().get("id")
                if new_id:
                    self.my_created_contacts.append(new_id)
            except Exception as e:
                print(f"Error adding new contact ID: {e}")
    
    @task(0)  # Disabled by default
    def update_contact(self):
        """Simulate updating an existing contact - disabled by default"""
        if not ENABLE_PATCH:
            return
            
        # Only update contacts this user created to avoid conflicts
        if not self.my_created_contacts:
            return
            
        contact_id = random.choice(self.my_created_contacts)
        updated_data = {
            "company": f"Updated Company {random.randint(1000, 9999)}",
            "notes": f"Updated during load testing at {time.time()}"
        }
        
        headers = {"Content-Type": "application/json"}
        response = self.client.patch(f"/contacts/{contact_id}", json=updated_data, headers=headers)
        
        # If we get a 404 or 422, remove it from our list
        if response.status_code in [404, 422]:
            if contact_id in self.my_created_contacts:
                self.my_created_contacts.remove(contact_id)
    
    @task(1)
    def delete_contact(self):
        """Simulate deleting a contact"""
        # Only delete contacts this user created
        if not self.my_created_contacts:
            return
            
        contact_id = random.choice(self.my_created_contacts)
        response = self.client.delete(f"/contacts/{contact_id}")
        
        # Remove from our list regardless of response
        if contact_id in self.my_created_contacts:
            self.my_created_contacts.remove(contact_id)
    
    @task(1)
    def health_check(self):
        """Occasionally check the health endpoint"""
        self.client.get("/health")

class APIMonitorUser(HttpUser):
    """A separate user class that focuses on monitoring endpoints"""
    wait_time = between(5, 15)  # Check less frequently
    
    @task
    def check_metrics(self):
        """Check the Prometheus metrics endpoint"""
        self.client.get("/metrics")
