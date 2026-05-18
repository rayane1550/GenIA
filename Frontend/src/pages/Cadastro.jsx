import "./Cadastro.css";
import { useState } from "react";
import { Link } from "react-router-dom";

import robot from "../assets/robot.svg";
import google from "../assets/google.png";

import Card from "../components/Card";
import Input from "../components/Input";
import Button from "../components/Button";

function Cadastro() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");

  // APENAS UMA DECLARAÇÃO DA FUNÇÃO AQUI:
  const handleCadastro = async () => {
    if (!username || !email || !password1 || !password2) {
      alert("Preencha todos os campos.");
      return;
    }

    if (password1 !== password2) {
      alert("As senhas não coincidem.");
      return;
    }

    try {
      const response = await fetch(
        "http://localhost:8000/api/auth/registration/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: username.trim(), // Remove espaços acidentais
            email: email,
            password1: password1, // Chave correta exigida pelo seu Django
            password2: password2,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        alert("Cadastro realizado com sucesso!");
        window.location.href = "/login";
      } else {
        console.log("Erros detalhados do Django:", data);
        
        let mensagensDeErro = "";
        Object.keys(data).forEach((campo) => {
          if (Array.isArray(data[campo])) {
            mensagensDeErro += `${campo}: ${data[campo].join(", ")}\n`;
          } else {
            mensagensDeErro += `${campo}: ${data[campo]}\n`;
          }
        });

        alert("Erro ao cadastrar:\n" + mensagensDeErro);
      }
    } catch (error) {
      console.error(error);
      alert("Erro ao conectar com servidor.");
    }
  };

  const handleGoogleCadastro = () => {
    window.location.href =
      "http://localhost:8000/accounts/google/login/?process=login";
  };

  return (
    <div className="container">
      <Card>
        <img src={robot} alt="robot" className="icon" />

        <h2>
          Bem vindo ao <span>CADASTRO</span>
        </h2>

        <Input
          type="text"
          placeholder="Name"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <Input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <Input
          type="password"
          placeholder="Password"
          value={password1}
          onChange={(e) => setPassword1(e.target.value)}
        />

        <Input
          type="password"
          placeholder="Confirm Password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
        />

        <div className="checkbox-area">
          <input type="checkbox" id="termos" />
          <label htmlFor="termos" style={{ cursor: "pointer" }}>
            Eu concordo com Termos e Condições
          </label>
        </div>

        <Button text="Cadastrar-se" onClick={handleCadastro} />

        <button
          className="google-btn"
          type="button"
          onClick={handleGoogleCadastro}
        >
          <img src={google} alt="google" />
          Continuar com Google
        </button>

        <p className="login-text">
          Já tem conta?{" "}
          <Link to="/login">
            <span>Entrar</span>
          </Link>
        </p>
      </Card>
    </div>
  );
}

export default Cadastro;