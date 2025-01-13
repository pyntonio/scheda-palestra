// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/register">Register</Link></li>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/change-password">Change Password</Link></li>
        <li><Link to="/secure-data">Secure Data</Link></li>
        <li><Link to="/oroscopo">Genera Oroscopo</Link></li>
        <li><Link to="/stripe">Abbonamento</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
