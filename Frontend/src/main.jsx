import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

import { Auth0Provider } from "@auth0/auth0-react";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>

    <Auth0Provider
      domain="geniatcc.uk.auth0.com"
      clientId="fcNck2hsBvG8G6UJZBeSX7AyLVnQpik8"
      authorizationParams={{
        redirect_uri: window.location.origin,
      }}
    >

      <App />

    </Auth0Provider>

  </React.StrictMode>
);