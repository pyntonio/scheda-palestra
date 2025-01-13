// src/components/Login.js
import React, { useState } from 'react';
import ENDPOINTS from '../config/apiConfig';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [token, setToken] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(ENDPOINTS.login, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: email,
          password,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setToken(data.access_token);
        localStorage.setItem('token', data.access_token);
      } else {
        setErrorMessage(data.detail);
      }
    } catch (err) {
      setErrorMessage('Something went wrong');
    }
  };

  return (
    <div className="register-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      {token && <p className="success-message">Logged in with token: {token}</p>}
    </div>
  );
};

export default Login;
