// src/config/apiConfig.js
const API_BASE_URL = 'http://127.0.0.1:8000';  // Assicurati che l'URL corrisponda al tuo backend

export const ENDPOINTS = {
  login: `${API_BASE_URL}/token`,
  changePassword: `${API_BASE_URL}/change-password`,
  secureData: `${API_BASE_URL}/secure-data`,
  generaOroscopo: `${API_BASE_URL}/genera_oroscopo/`,
  register: `${API_BASE_URL}/register/`,
};

export default ENDPOINTS;
