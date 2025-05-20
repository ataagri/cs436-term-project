import React, { useEffect, useState } from 'react';
import { useAuth } from './auth/AuthContext';

import PhoneLayout from './layouts/phoneLayout';
import AddContact from './addContact';
import ShowContact from './showContact';

export default function AllContacts() {
  let [contacts, setContacts] = useState([]);
  let [showContact, setShowContact] = useState(null);
  const { currentUser } = useAuth();

  useEffect(() => {
    // Get the token from the current user
    const getIdToken = async () => {
      if (!currentUser) return null;
      try {
        return await currentUser.getIdToken();
      } catch (error) {
        console.error('Error getting token:', error);
        return null;
      }
    };

    const fetchContacts = async () => {
      try {
        const token = await getIdToken();
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        
        const response = await fetch(`${process.env.REACT_APP_API_URL}/all-contacts`, {
          headers
        });
        
        if (response.ok) {
          const data = await response.json();
          setContacts(data);
        } else {
          console.error('Failed to fetch contacts:', response.status);
        }
      } catch (err) {
        console.error('Error fetching contacts:', err);
      }
    };

    fetchContacts();
  }, [currentUser]);

  return (
    <PhoneLayout>
      <div className="relative">
        <AddContact />
        <div className="flex flex-col">
          {contacts.map((contact) => (
            <div key={contact.id}>
              {showContact === contact.id ? (
                <ShowContact contactId={contact.id} open={true} />
              ) : (
                <div
                  className="border-b border-slate-200 p-4 py-2 text-left capitalize text-slate-700 hover:bg-slate-200"
                  onClick={() =>
                    setShowContact((show) =>
                      show === contact.id ? null : contact.id
                    )
                  }
                >
                  <span className="font-bold">{contact.first_name}</span>{' '}
                  {contact.last_name}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </PhoneLayout>
  );
}
