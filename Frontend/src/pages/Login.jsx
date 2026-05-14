import "./Login.css";

import { useState } from "react";

import robot from "../assets/robot.svg";
import google from "../assets/google.png";

import Card from "../components/Card";
import Input from "../components/Input";
import Button from "../components/Button";

import { useAuth0 } from "@auth0/auth0-react";

function Login() {

  const { loginWithRedirect } = useAuth0();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/login/",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            email,
            password,
          }),
        }
      );

      const data = await response.json();

      console.log(data);

      alert("Login realizado!");

    } catch (error) {
      console.log(error);
    }
  };

  const handleGoogleLogin = () => {

    loginWithRedirect({
      authorizationParams: {
        connection: "google-oauth2",
      },
    });

  };

  return (
    <div className="container">

      <Card>

        <img
          src={robot}
          alt="robot"
          className="icon"
        />

        <h2>
          Bem vindo ao <span>GEN IA</span>
        </h2>

        <Input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <span className="forgot">
          esqueci minha senha
        </span>

        <Button
          text="Entrar"
          onClick={handleLogin}
        />

        <button
          className="google-btn"
          onClick={handleGoogleLogin}
        >

          <img
            src={google}
            alt="google"
          />

          Continuar com Google

        </button>

        <p className="signup">
          Não tem conta?
          <span> Criar uma conta</span>
        </p>

      </Card>

    </div>
  );
}

export default Login;