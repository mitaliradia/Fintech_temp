import React from "react";
import ReactDOM from "react-dom/client"; // ✅ Ensure this is correct
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import "./index.css";
import 'bootstrap/dist/css/bootstrap.min.css';


ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);

