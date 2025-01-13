// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import ChangePassword from './components/ChangePassword';
import SecureData from './components/SecureData';
import Oroscopo from './components/Oroscopo';
import Register from './components/Register'; // Assicurati che il percorso del file sia corretto
import Stripe from './components/Stripe';
import './App.css';

const App = () => {
  return (
    <Router>
      <Navbar />
      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/change-password" element={<ChangePassword />} />
          <Route path="/secure-data" element={<SecureData />} />
          <Route path="/oroscopo" element={<Oroscopo />} />
          <Route path="/stripe" element={<Stripe />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
