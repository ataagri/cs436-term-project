// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDmwft79Ti1jHi6wZ7tuJuCf9lIBzF5Hu0",
  authDomain: "cs436-reactfastcontacts.firebaseapp.com",
  projectId: "cs436-reactfastcontacts",
  storageBucket: "cs436-reactfastcontacts.firebasestorage.app",
  messagingSenderId: "908441703174",
  appId: "1:908441703174:web:6ba1c8dd6b2dd7ce450487",
  measurementId: "G-WS7PTPLMKE"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

export { auth };
export default app;