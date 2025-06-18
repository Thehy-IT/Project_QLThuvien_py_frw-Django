/**
 * @file index.tsx
 * This is the main entry point for the React application.
 * It renders the root <App /> component into the DOM.
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Get the root DOM element where the React app will be mounted.
const rootElement = document.getElementById('root');

// Ensure the root element exists before attempting to render the app.
if (!rootElement) {
  throw new Error("Could not find root element to mount to");
}

// Create a React root for concurrent mode features.
const root = ReactDOM.createRoot(rootElement);

// Render the main App component within React.StrictMode for highlighting potential problems.
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);