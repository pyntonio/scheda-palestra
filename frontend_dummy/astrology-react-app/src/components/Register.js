// src/components/Register.js
import React, { useState } from 'react';
import { ENDPOINTS } from '../config/apiConfig';  // Importa gli endpoint

const Register = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Reset dei messaggi
        setErrorMessage('');
        setSuccessMessage('');

        const userData = {
            email: email,
            username: username,
            password: password
        };

        try {
            const response = await fetch(ENDPOINTS.register, {  // Usa l'endpoint per la registrazione
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            });

            const data = await response.json();

            if (response.ok) {
                setSuccessMessage('User registered successfully! Please check your email to confirm your account.');
            } else {
                setErrorMessage(data.detail || 'Error occurred during registration.');
            }
        } catch (error) {
            setErrorMessage('An error occurred while trying to register.');
        }
    };

    return (
        <div className="register-container">
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Register</button>
            </form>

            {errorMessage && <p className="error-message">{errorMessage}</p>}
            {successMessage && <p className="success-message">{successMessage}</p>}
        </div>
    );
};

export default Register;
