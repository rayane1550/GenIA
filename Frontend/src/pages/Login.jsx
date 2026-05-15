import "./Login.css";
import { useState } from "react";
import robot from "../assets/robot.svg";
import google from "../assets/google.png";
import Card from "../components/Card";
import Input from "../components/Input";
import Button from "../components/Button";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    if (!email || !password) {
      alert("Por favor, preencha todos os campos.");
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/auth/login/", 
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: email, // O dj-rest-auth espera 'username' por padrão
            password: password,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        console.log("Sucesso:", data);
        
        // Armazena o token JWT que vem do dj-rest-auth
        // Geralmente vem como data.access ou data.access_token conforme sua config
        const token = data.access || data.access_token || data.key;
        localStorage.setItem("token", token);
        
        alert("Login realizado com sucesso!");
        // window.location.href = "/home"; // Redirecione para sua rota interna aqui
      } else {
        alert(data.non_field_errors || "E-mail ou senha incorretos.");
      }
    } catch (error) {
      console.error("Erro na conexão:", error);
      alert("Não foi possível conectar ao servidor.");
    }
  };

  const handleGoogleLogin = () => {
    /** * O segredo está no ?process=login ao final da URL.
     * Isso instrui o Allauth a ir direto para o Google sem passar 
     * pela página intermediária do Django.
     */
    window.location.href = "http://127.0.0.1:8000/accounts/google/login/?process=login";
  };

  return (
    <div className="container">
      <Card>
        <img src={robot} alt="robot" className="icon" />
        <h2>Bem vindo ao <span>LOGIN</span></h2>

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

        <span className="forgot">esqueci minha senha</span>

        <Button text="Entrar" onClick={handleLogin} />

        <button className="google-btn" type="button" onClick={handleGoogleLogin}>
          <img src={google} alt="google" />
          Continuar com Google
        </button>

        <p className="signup">
          Não tem conta? <span> Criar uma conta</span>
        </p>
      </Card>
    </div>
  );
}

export default Login;