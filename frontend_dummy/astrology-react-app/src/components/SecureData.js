// src/components/SecureData.js
import React, { useState, useEffect } from 'react';
import ENDPOINTS from '../config/apiConfig';

const SecureData = () => {
  const [data, setData] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem('token');

      if (!token) {
        setErrorMessage('You need to login first.');
        return;
      }

      try {
        const response = await fetch(ENDPOINTS.secureData, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          setData(data);
        } else {
          setErrorMessage(data.detail);
        }
      } catch (err) {
        setErrorMessage('Something went wrong');
      }
    };

    fetchData();
  }, []);

  return (
    <div className="secure-data">
      <h2>Secure Data</h2>
      {errorMessage && <p className="error">{errorMessage}</p>}
      {data && (
        <div>
          <p>{data.message}</p>
          <p>Email: {data.email}</p>
          <p>Created At: {data.created_at}</p>
          <p>Verified: {data.is_verified ? 'Yes' : 'No'}</p>
        </div>
      )}
    </div>
  );
};

export default SecureData;
