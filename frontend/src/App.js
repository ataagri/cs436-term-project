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