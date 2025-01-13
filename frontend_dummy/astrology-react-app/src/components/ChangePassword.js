// src/components/ChangePassword.js
import React, { useState } from 'react';
import ENDPOINTS from '../config/apiConfig';

const ChangePassword = () => {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleChangePassword = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');

    if (!token) {
      setErrorMessage('You need to login first.');
      return;
    }

    try {
      const response = await fetch(ENDPOINTS.changePassword, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setSuccessMessage(data.message);
        setCurrentPassword('');
        setNewPassword('');
      } else {
        setErrorMessage(data.detail);
      }
    } catch (err) {
      setErrorMessage('Something went wrong');
    }
  };

  return (
    <div className="change-password">
      <h2>Change Password</h2>
      <form onSubmit={handleChangePassword}>
        <input
          type="password"
          placeholder="Current Password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="New Password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
        />
        <button type="submit">Change Password</button>
      </form>
      {errorMessage && <p className="error">{errorMessage}</p>}
      {successMessage && <p>{successMessage}</p>}
    </div>
  );
};

export default ChangePassword;
