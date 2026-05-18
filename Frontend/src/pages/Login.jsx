import "./Login.css";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom"; // Importado useNavigate para o fluxo funcionar

import robot from "../assets/robot.svg";
import google from "../assets/google.png";
import Card from "../components/Card";
import Input from "../components/Input";
import Button from "../components/Button";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // ESTADOS DE ERRO VISUAL
  const [errorEmail, setErrorEmail] = useState("");
  const [errorPassword, setErrorPassword] = useState("");
  const [errorGeral, setErrorGeral] = useState("");

  // Função simples para validar e-mail no front-end antes de mandar pro Django
  const validarEmail = (emailStr) => {
    return /\S+@\S+\.\S+/.test(emailStr);
  };

  const handleLogin = async () => {
    // Resetando erros anteriores ao tentar logar de novo
    setErrorEmail("");
    setErrorPassword("");
    setErrorGeral("");

    let erroDetectado = false;

    // 1. Validação de Campos Vazios
    if (!email && !password) {
      setErrorGeral("Preencha todos os campos");
      return;
    }

    if (!email) {
      setErrorEmail("O campo de e-mail é obrigatório");
      erroDetectado = true;
    } else if (!validarEmail(email)) {
      // 2. Validação de Formato de E-mail (Ex: "Gabriela@")
      setErrorEmail("Digite um email válido");
      erroDetectado = true;
    }

    if (!password) {
      setErrorPassword("O campo de senha é obrigatório");
      erroDetectado = true;
    }

    if (erroDetectado) return;

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/auth/login/", 
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: email,
            password: password,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        console.log("Sucesso:", data);
        const token = data.access || data.access_token || data.key;
        localStorage.setItem("token", token);
        
        // Redireciona direto para o chat se der boa
        navigate("/chat"); 
      } else {
        // 3. Validação vinda do Backend (Credenciais erradas)
        setErrorGeral("Email ou senha incorretos");
      }
    } catch (error) {
      console.error("Erro na conexão:", error);
      setErrorGeral("Não foi possível conectar ao servidor.");
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = "http://127.0.0.1:8000/accounts/google/login/?process=login";
  };

  return (
    <div className="container">
      <Card>
        <img src={robot} alt="robot" className="icon" />
        <h2>Bem vindo ao <span>LOGIN</span></h2>

        {/* MENSAGEM DE ERRO GERAL (Preencha todos os campos / Incorretos) */}
        {errorGeral && <span className="error-message-inline geral">{errorGeral}</span>}

        {/* INPUT EMAIL COM VALIDAÇÃO INLINE */}
        <div className="input-group-validation">
          {errorEmail && <span className="error-message-inline">{errorEmail}</span>}
          <div className={errorEmail ? "input-error-wrapper" : ""}>
            <Input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if(errorEmail) setErrorEmail(""); // Limpa o erro enquanto digita
              }}
            />
          </div>
        </div>

        {/* INPUT PASSWORD COM VALIDAÇÃO INLINE */}
        <div className="input-group-validation">
          {errorPassword && <span className="error-message-inline">{errorPassword}</span>}
          <div className={errorPassword ? "input-error-wrapper" : ""}>
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                if(errorPassword) setErrorPassword(""); // Limpa o erro enquanto digita
              }}
            />
          </div>
        </div>

        <span className="forgot">esqueci minha senha</span>

        <Button text="Entrar" onClick={handleLogin} />

        <button className="google-btn" type="button" onClick={handleGoogleLogin}>
          <img src={google} alt="google" />
          Continuar com Google
        </button>

        <p className="signup">
          Não tem conta?
          <Link to="/cadastro">
            <span> Criar uma conta</span>
          </Link>
        </p>
      </Card>
    </div>
  );
}

export default Login;