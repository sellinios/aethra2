import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { isAxiosError } from '../utils/axios.Error'; // Correct import path
import { AxiosError } from 'axios';

interface AxiosErrorData {
    detail?: string;
}

const Login: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await api.post('/users/login/', {
                username,
                password,
            });
            console.log('Login successful', response.data);
            localStorage.setItem('access', response.data.access);
            localStorage.setItem('refresh', response.data.refresh);
            navigate('/');
        } catch (err) {
            if (isAxiosError(err)) {
                const data: AxiosErrorData = err.response?.data || {};
                setError(data.detail || 'Invalid username or password');
            } else {
                setError('Error logging in');
            }
            console.error('Error logging in', err);
        }
    };

    return (
        <div className="container mt-3">
            <h2>Login</h2>
            {error && <p className="text-danger">{error}</p>}
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Username</label>
                    <input
                        type="text"
                        className="form-control"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label>Password</label>
                    <input
                        type="password"
                        className="form-control"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
        </div>
    );
};

export default Login;