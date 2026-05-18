import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Welcome from './pages/Welcome'; // Importe a nova tela
import Login from './pages/Login';
import Cadastro from './pages/Cadastro';

function App() {
  return (
    <Router>
      <Routes>
        {/* Agora a rota raiz abre o carrossel */}
        <Route path="/" element={<Welcome />} />
        
        {/* O login fica mapeado na rota secundária */}
        <Route path="/login" element={<Login />} />
        
        <Route path="/cadastro" element={<Cadastro />} />
      </Routes>
    </Router>
  );
}

export default App;