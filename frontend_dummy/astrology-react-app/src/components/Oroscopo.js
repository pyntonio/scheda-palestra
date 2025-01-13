import React, { useState } from 'react';
import ENDPOINTS from '../config/apiConfig';
import ReactMarkdown from 'react-markdown'; // Importa react-markdown

const Oroscopo = () => {
  const [data, setData] = useState({
    nome: '',
    data_nascita: '',
    ora_nascita: '',
    luogo_nascita: '',
  });
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false); // Stato per gestire il caricamento

  // Funzione per aggiornare lo stato dei dati dell'utente
  const handleChange = (e) => {
    const { name, value } = e.target;
    setData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Funzione per generare l'oroscopo
  const handleGenerateOroscopo = async () => {
    setLoading(true);  // Avvia lo spinner
    try {
      const response = await fetch(ENDPOINTS.generaOroscopo, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      if (response.ok) {
        setResult(result);
      } else {
        setErrorMessage(result.detail);
      }
    } catch (err) {
      setErrorMessage('Something went wrong');
    } finally {
      setLoading(false); // Ferma lo spinner
    }
  };

  return (
    <div className="oroscopo">
      <h2>Genera Oroscopo</h2>

      {/* Input per il nome */}
      <label>
        Nome:
        <input
          type="text"
          name="nome"
          value={data.nome}
          onChange={handleChange}
        />
      </label>
      <br />

      {/* Input per la data di nascita */}
      <label>
        Data di nascita:
        <input
          type="date"
          name="data_nascita"
          value={data.data_nascita}
          onChange={handleChange}
        />
      </label>
      <br />

      {/* Input per l'ora di nascita */}
      <label>
        Ora di nascita:
        <input
          type="time"
          name="ora_nascita"
          value={data.ora_nascita}
          onChange={handleChange}
        />
      </label>
      <br />

      {/* Input per il luogo di nascita */}
      <label>
        Luogo di nascita:
        <input
          type="text"
          name="luogo_nascita"
          value={data.luogo_nascita}
          onChange={handleChange}
        />
      </label>
      <br />

      {/* Bottone per generare l'oroscopo */}
      <button onClick={handleGenerateOroscopo}>Genera Oroscopo</button>

      {/* Mostra lo spinner durante il caricamento */}
      {loading && <div className="spinner"></div>}

      {/* Visualizza eventuali messaggi di errore */}
      {errorMessage && <p className="error">{errorMessage}</p>}

      {/* Visualizza il risultato dell'oroscopo in Markdown convertito */}
      {result && (
        <div className="oroscopo-result">
          <h3>Oroscopo:</h3>
          {/* Usa react-markdown per rendere il testo Markdown */}
          <ReactMarkdown>{result.oroscopo_text}</ReactMarkdown>
          <a href={`/pdf/${result.pdf_filename}`} target="_blank" rel="noopener noreferrer">
            Download PDF
          </a>
        </div>
      )}
    </div>
  );
};

export default Oroscopo;
