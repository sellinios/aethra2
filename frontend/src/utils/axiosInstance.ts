import axios from 'axios';

console.log("Backend URL: ", process.env.REACT_APP_BACKEND_URL);

const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL || 'https://kairos.gr/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
