// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import Header from "./pages/Header.js";
import BlockchainIntegration from "./pages/BlockchainIntegration.js";
import CompatibilityCheck from "./pages/CompatibilityCheck.js";
import Contact from "./pages/Contact.js";
import Home from "./pages/Home.js";
import FormPage from "./pages/FormPage.js";
import ResultPage from "./pages/ResultPage.js";
import About from "./pages/About.js";
import Footer from './pages/Footer.js';
import "./App.css";

function ProtectedRoute({ element }) {
  const { isAuthenticated, isLoading, loginWithRedirect } = useAuth0();

  if (isLoading) return <h2>Loading...</h2>;
  
  if (!isAuthenticated) {
    loginWithRedirect({ authorizationParams: { redirect_uri: window.location.origin + "/result" } });  
    return null; 
  }

  return element;
}

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/about" element={<About />} />
        
        {/* Protect these pages */}
        <Route path="/form" element={<ProtectedRoute element={<FormPage />} />} />
        <Route path="/result" element={<ProtectedRoute element={<ResultPage />} />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
