import React from "react";
import Navbar from "./components/Navbar";
import { Routes, Route, useLocation } from "react-router-dom";

import HomePage from "./pages/HomePage";
import FeaturedProductsPage from "./pages/FeaturedProductsPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";

import Footer from "./components/Footer";

function App() {

  const location = useLocation();

  const hideLayout =
    location.pathname === "/login" ||
    location.pathname === "/register" ||
    location.pathname === "/forgot-password";

  return (
    <>
      {/* Navbar */}
      <Navbar hideSearch={hideLayout} />
      
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/products" element={<FeaturedProductsPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      </Routes>

      {/* Footer */}
      {!hideLayout && <Footer />}
    </>
  );
}

export default App;