import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './i18n'; // Ensure this is imported

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container!); // Add non-null assertion (!)
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);