// api.js

import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'kairos.gr',  // Ensure this matches your backend URL
});

export default api;