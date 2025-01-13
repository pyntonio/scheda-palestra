Per creare un'app React scalabile che gestisce i vari endpoint FastAPI, segui questa struttura di base. L'app includerà una navigazione tra le diverse funzionalità, un file di configurazione per gli endpoint e una grafica gradevole usando CSS.

### 1. **Installazione di React e Creazione del Progetto**

Prima di iniziare, crea un nuovo progetto React utilizzando `create-react-app` (se non l'hai già fatto):

```bash
npx create-react-app astrology-react-app
cd astrology-react-app
npm start
```

### 2. **Struttura del Progetto**

Organizza la tua applicazione con una struttura chiara:

```
oroscopi-app/
│
├── src/
│   ├── components/
│   │   ├── Navbar.js
│   │   ├── Home.js
│   │   ├── Login.js
│   │   ├── ChangePassword.js
│   │   ├── SecureData.js
│   │   └── Oroscopo.js
│   ├── config/
│   │   └── apiConfig.js
│   ├── App.js
│   ├── index.js
│   └── App.css
└── package.json
```

### 3. **File di Configurazione degli Endpoint (apiConfig.js)**

Crea un file di configurazione per gestire gli URL degli endpoint:

```javascript
// src/config/apiConfig.js
const API_BASE_URL = 'http://127.0.0.1:8000';  // Assicurati che l'URL corrisponda al tuo backend

export const ENDPOINTS = {
  login: `${API_BASE_URL}/token`,
  changePassword: `${API_BASE_URL}/change-password`,
  secureData: `${API_BASE_URL}/secure-data`,
  generaOroscopo: `${API_BASE_URL}/genera_oroscopo/`,
};

export default ENDPOINTS;
```

### 4. **Componente Navbar (Navbar.js)**

Questo componente mostrerà un menu di navigazione con le varie funzionalità.

```javascript
// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/change-password">Change Password</Link></li>
        <li><Link to="/secure-data">Secure Data</Link></li>
        <li><Link to="/oroscopo">Genera Oroscopo</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
```

### 5. **Componente Home (Home.js)**

Componente che mostra la pagina principale.

```javascript
// src/components/Home.js
import React from 'react';

const Home = () => {
  return (
    <div className="home">
      <h1>Welcome to the Oroscopo App</h1>
      <p>Choose a functionality from the menu above.</p>
    </div>
  );
};

export default Home;
```

### 6. **Componente Login (Login.js)**

Componente per il login dell'utente.

```javascript
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
    <div className="login">
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
      {errorMessage && <p className="error">{errorMessage}</p>}
      {token && <p>Logged in with token: {token}</p>}
    </div>
  );
};

export default Login;
```

### 7. **Componente ChangePassword (ChangePassword.js)**

Permette agli utenti di cambiare la loro password.

```javascript
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
```

### 8. **Componente SecureData (SecureData.js)**

Mostra i dati protetti dell'utente.

```javascript
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
```

### 9. **Componente Oroscopo (Oroscopo.js)**

Componente per generare l'oroscopo.

```javascript
// src/components/Oroscopo.js
import React, { useState } from 'react';
import ENDPOINTS from '../config/apiConfig';

const Oroscopo = () => {
  const [data, setData] = useState({});
  const [result,

 setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleGenerateOroscopo = async () => {
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
    }
  };

  return (
    <div className="oroscopo">
      <h2>Genera Oroscopo</h2>
      <button onClick={handleGenerateOroscopo}>Genera Oroscopo</button>
      {errorMessage && <p className="error">{errorMessage}</p>}
      {result && (
        <div>
          <h3>Oroscopo:</h3>
          <p>{result.oroscopo_text}</p>
          <a href={`/pdf/${result.pdf_filename}`} target="_blank" rel="noopener noreferrer">
            Download PDF
          </a>
        </div>
      )}
    </div>
  );
};

export default Oroscopo;
```

### 10. **App.js (Routing e Navigazione)**

```javascript
// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import ChangePassword from './components/ChangePassword';
import SecureData from './components/SecureData';
import Oroscopo from './components/Oroscopo';
import './App.css';

const App = () => {
  return (
    <Router>
      <Navbar />
      <div className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/change-password" element={<ChangePassword />} />
          <Route path="/secure-data" element={<SecureData />} />
          <Route path="/oroscopo" element={<Oroscopo />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
```

### 11. **App.css (Stili Base)**

```css
/* src/App.css */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

.navbar {
  background-color: #333;
  color: white;
  padding: 10px 0;
  text-align: center;
}

.navbar ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

.navbar ul li {
  display: inline;
  margin: 0 20px;
}

.navbar a {
  color: white;
  text-decoration: none;
}

.content {
  padding: 20px;
}

.error {
  color: red;
}
```

### 12. **Conclusione**

Ora hai un'app React scalabile che può comunicare con il tuo backend FastAPI. Ogni componente è separato e facilmente mantenibile, con un file di configurazione per gli endpoint. La navigazione è gestita tramite `react-router-dom`, e la grafica è semplice ma gradevole. Puoi migliorare ulteriormente lo stile e aggiungere altre funzionalità a seconda delle necessità.