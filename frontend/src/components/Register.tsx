// src/components/Register.tsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register: React.FC = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [preferredLanguage, setPreferredLanguage] = useState('en');
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await axios.post('/users/register/', {
                username,
                email,
                password,
                preferred_language: preferredLanguage,
            });
            navigate('/login');
        } catch (error) {
            console.error('Error registering', error);
        }
    };

    return (
        <div className="container mt-3">
            <h2>Register</h2>
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
                    <label>Email</label>
                    <input
                        type="email"
                        className="form-control"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
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
                <div className="form-group">
                    <label>Preferred Language</label>
                    <select
                        className="form-control"
                        value={preferredLanguage}
                        onChange={(e) => setPreferredLanguage(e.target.value)}
                    >
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        {/* Add more languages as needed */}
                    </select>
                </div>
                <button type="submit" className="btn btn-primary">Register</button>
            </form>
        </div>
    );
};

export default Register;