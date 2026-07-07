import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import App from "./App";
import "./styles/global.css";
import "./styles/auth.css";
import "./styles/layout.css";
import "./styles/feature.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <ToastContainer
      position="top-right"
      autoClose={2500}
      hideProgressBar={false}
      newestOnTop
      closeOnClick
      pauseOnHover
      theme="light"
    />

    <App />
  </BrowserRouter>,
);
