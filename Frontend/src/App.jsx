import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Welcome from './pages/Welcome';
import Login from './pages/Login';
import Cadastro from './pages/Cadastro';
import ForgotPassword from './pages/ForgotPassword';
import ChatGeral from './pages/ChatGeral';

function ProtectedRoute({ children }) {
  // 1. Tenta pegar o token tradicional do localStorage
  const token = localStorage.getItem("token");
  
  // 2. Tenta verificar se existe o Cookie de sessão que o Django acabou de criar
  const temCookieDjango = document.cookie.split(';').some((item) => item.trim().startsWith('sessionid='));

  // Se tiver o token OU tiver o cookie do Django, o guardião libera a entrada!
  if (!token && !temCookieDjango) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function LoginCallback() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const token = queryParams.get('token') || queryParams.get('key'); // Depende de como o seu Django envia o token

    if (token) {
      localStorage.setItem("token", token);
      navigate("/chat", { replace: true });
    } else {
      navigate("/login", { replace: true });
    }
  }, [navigate, location]);

  return <div>Carregando sua sessão...</div>;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/esqueci-senha" element={<ForgotPassword />} />
        
        {/* Rota temporária para salvar o token do Google */}
        <Route path="/login-callback" element={<LoginCallback />} />
        
        <Route 
          path="/chat" 
          element = {
            <ProtectedRoute>
              <ChatGeral />
            </ProtectedRoute>
          } 
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;