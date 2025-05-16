# Firebase Authentication and Hosting Setup

## 1. Set Up Firebase Authentication

After setting up Firebase for your project as mentioned in `01-project-setup.md`, configure authentication:

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to "Authentication" in the left sidebar
4. Click on the "Sign-in method" tab
5. Enable "Email/Password" provider
6. Optionally, enable other providers (Google, GitHub, etc.)

## 2. Create a Firebase Web App

1. In the Firebase Console, go to "Project settings" (gear icon)
2. Under "Your apps", click "Add app" and select "Web"
3. Enter a nickname for your app (e.g., "Contacts Web App")
4. Click "Register app"
5. Copy the Firebase configuration object for later use

## 3. Install Firebase in the Frontend Project

Navigate to the frontend directory and install Firebase packages:

```bash
# Navigate to the frontend directory
cd /Users/ataagri/sabanci/cs436/cs436-term-project/frontend

# Install Firebase packages
npm install firebase firebase-auth
```

## 4. Create Firebase Configuration File

Create a Firebase configuration file:

```bash
# Create Firebase config file
touch /Users/ataagri/sabanci/cs436/cs436-term-project/frontend/src/firebase.js
```

Add the following content to the firebase.js file, replacing the configuration with your own:

```javascript
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };
export default app;
```

## 5. Create Authentication Components

Create authentication components for sign-in and sign-up:

### 5.1. Create SignIn Component

```bash
# Create SignIn component
mkdir -p /Users/ataagri/sabanci/cs436/cs436-term-project/frontend/src/components/auth
touch /Users/ataagri/sabanci/cs436/cs436-term-project/frontend/src/components/auth/SignIn.jsx
```

Add the following content to SignIn.jsx:

```jsx
import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../../firebase';

export default function SignIn({ onSignIn }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSignIn = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      if (onSignIn) onSignIn(user);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 rounded-lg bg-white shadow-md w-full max-w-md">
      <h2 className="text-2xl font-bold mb-6">Sign In</h2>
      
      {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 w-full">{error}</div>}
      
      <form onSubmit={handleSignIn} className="w-full">
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
            Email
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="email"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
            Password
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="password"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        
        <div className="flex items-center justify-between">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            Sign In
          </button>
        </div>
      </form>
    </div>
  );
}
```

### 5.2. Create SignUp Component

```bash
# Create SignUp component
touch /Users/ataagri/sabanci/cs436/cs436-term-project/frontend/src/components/auth/SignUp.jsx
```

Add the following content to SignUp.jsx:

```jsx
import React, { useState } from 'react';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../../firebase';

export default function SignUp({ onSignUp }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  const handleSignUp = async (e) => {
    e.preventDefault();
    setError('');
    
    if (password !== confirmPassword) {
      setError("Passwords don't match");
      return;
    }
    
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      if (onSignUp) onSignUp(user);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 rounded-lg bg-white shadow-md w-full max-w-md">
      <h2 className="text-2xl font-bold mb-6">Sign Up</h2>
      
      {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 w-full">{error}</div>}
      
      <form onSubmit={handleSignUp} className="w-full">
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
            Email
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="email"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
            Password
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="password"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="confirm-password">
            Confirm Password
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="confirm-password"
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        
        <div className="flex items-center justify-between">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            Sign Up
          </button>
        </div>
      </form>
    </div>
  );
}
```

### 5.3. Create AuthContext for Authentication State

```bash
# Create AuthContext
touch /Users/ataagri/sabanci/cs436/cs436-term-project/frontend/src/components/auth/AuthContext.jsx
```

Add the following content to AuthContext.jsx:

```jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { auth } from '../../firebase';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const logout = () => {
    return signOut(auth);
  };

  const value = {
    currentUser,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}
```

## 6. Update App.js to Include Authentication

Modify App.js to include authentication:

```jsx
import './input.css';
import { Helmet } from 'react-helmet';
import { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './components/auth/AuthContext';

import Contacts from './components/allContacts';
import Footer from './components/base/footer';
import SignIn from './components/auth/SignIn';
import SignUp from './components/auth/SignUp';

function AppContent() {
  const { currentUser, logout } = useAuth();
  const [showSignUp, setShowSignUp] = useState(false);

  const handleSignIn = (user) => {
    console.log('User signed in:', user);
  };

  const handleSignUp = (user) => {
    console.log('User signed up:', user);
    setShowSignUp(false);
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return (
    <div className="flex min-h-screen flex-col">
      <Helmet>
        <title>FastAPI Contact Book</title>
      </Helmet>
      <main className="flex grow justify-center px-4">
        <div className="prose p-10">
          <div className="flex items-center justify-center">
            <svg
              role="img"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              className="mr-2 h-8 w-8 fill-[#009688]"
            >
              <title>FastAPI</title>
              <path d="M12 0C5.375 0 0 5.375 0 12c0 6.627 5.375 12 12 12 6.626 0 12-5.373 12-12 0-6.625-5.373-12-12-12zm-.624 21.62v-7.528H7.19L13.203 2.38v7.528h4.029L11.376 21.62z" />
            </svg>
            <h1 className="m-0">ReactFast Contacts</h1>
            {currentUser && (
              <button 
                onClick={handleLogout}
                className="ml-4 bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded text-sm"
              >
                Logout
              </button>
            )}
          </div>

          <div className="flex justify-evenly">
            <img
              src="https://img.shields.io/badge/react-35495e.svg?&style=for-the-badge&logo=react&logoColor=61DAFB"
              alt="React"
            />
            <img
              src="https://img.shields.io/badge/tailwindcss-gray.svg?&style=for-the-badge&logo=tailwindcss&logoColor=06B6D4"
              alt="TailWindCSS"
            />
            <img
              src="https://img.shields.io/badge/fastapi-009688.svg?&style=for-the-badge&logo=fastapi&logoColor=white"
              alt="FastAPI"
            />
            <img
              src="https://img.shields.io/badge/firebase-FFCA28.svg?&style=for-the-badge&logo=firebase&logoColor=black"
              alt="Firebase"
            />
          </div>
          <div className="flex justify-center">
            {currentUser ? (
              <Contacts />
            ) : (
              <div className="flex flex-col items-center w-full">
                {showSignUp ? (
                  <>
                    <SignUp onSignUp={handleSignUp} />
                    <p className="mt-4">
                      Already have an account?{' '}
                      <button
                        className="text-blue-500 hover:text-blue-700"
                        onClick={() => setShowSignUp(false)}
                      >
                        Sign In
                      </button>
                    </p>
                  </>
                ) : (
                  <>
                    <SignIn onSignIn={handleSignIn} />
                    <p className="mt-4">
                      Don't have an account?{' '}
                      <button
                        className="text-blue-500 hover:text-blue-700"
                        onClick={() => setShowSignUp(true)}
                      >
                        Sign Up
                      </button>
                    </p>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
```

## 7. Update API Calls with Authentication

Update API calls to include the authentication token in headers:

```jsx
// Example updated fetch call in allContacts.jsx
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
      return await currentUser.getIdToken();
    };

    const fetchContacts = async () => {
      try {
        const token = await getIdToken();
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        
        const response = await fetch('https://api.YOUR_DOMAIN.com/all-contacts', {
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

  // Rest of the component remains the same
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
```

## 8. Deploy to Firebase Hosting

### 8.1. Install Firebase CLI

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login to Firebase
firebase login
```

### 8.2. Initialize Firebase Hosting

```bash
# Navigate to the frontend directory
cd /Users/ataagri/sabanci/cs436/cs436-term-project/frontend

# Initialize Firebase
firebase init
```

Select the following options:
- Select "Hosting: Configure and deploy Firebase Hosting sites"
- Select your project
- Use "build" as the public directory
- Configure as a single-page app
- Don't overwrite index.html

### 8.3. Update Environment Variables

Create a .env file for environment variables:

```bash
# Create .env file
touch /Users/ataagri/sabanci/cs436/cs436-term-project/frontend/.env
```

Add the following content to the .env file:

```
REACT_APP_API_URL=https://api.YOUR_DOMAIN.com
```

Update your API call URLs to use the environment variable:

```javascript
// Example in allContacts.jsx
fetch(`${process.env.REACT_APP_API_URL}/all-contacts`, {
  headers
})
```

### 8.4. Build and Deploy

```bash
# Build the production version
npm run build

# Deploy to Firebase Hosting
firebase deploy
```

Replace `YOUR_DOMAIN.com` with your actual domain or use the Firebase Hosting default domain (e.g., `YOUR_PROJECT_ID.web.app`).