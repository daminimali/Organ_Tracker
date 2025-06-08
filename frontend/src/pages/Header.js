// src/Header.js
import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate, useLocation } from "react-router-dom";
import "../styles/Header.css";

function Header() {
  const { loginWithRedirect, isAuthenticated, logout, user, getAccessTokenSilently } = useAuth0();
  const navigate = useNavigate();
  const location = useLocation(); // 🧠 Get current path

  const currentPath = location.pathname;

  const handleDeleteAccount = async () => {
    try {
      const userId = user?.nickname || user?.sub?.split("|")[1];  
      const auth0Id = user?.sub;
  
      if (!userId || !auth0Id) return alert("Invalid user info");
  
      const accessToken = await getAccessTokenSilently({
        authorizationParams: {
          audience: "https://dev-o6a67bnmtfoq8kfc.us.auth0.com/api/v2/",
        },
      });
  
      const res = await fetch("http://localhost:8080/delete-user", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ userId, auth0Id }),
      });
  
      const data = await res.json();
  
      if (!res.ok) {
        console.error("Backend error:", data.error || data.message);
        alert("Something went wrong while deleting the account.");
        return;
      }
  
      alert("Account deleted successfully");
      logout({ returnTo: window.location.origin });
    } catch (error) {
      console.error("Frontend error deleting account:", error);
      alert("Something went wrong while deleting the account.");
    }
  };

  return (
    <header className="header">
      <h1 className="header-logo" onClick={() => navigate("/")}>Organ Tracker</h1>
      <nav className="header-nav">
        {isAuthenticated && <span className="user-welcome">Hi, {user.name}!</span>}

        <button
          onClick={() => navigate("/")}
          className={`nav-btn ${currentPath === "/" ? "active" : ""}`}
        >
          Home
        </button>

        <button
          onClick={() => navigate("/about")}
          className={`nav-btn ${currentPath === "/about" ? "active" : ""}`}
        >
          About
        </button>

        <button
          onClick={() => navigate("/contact")}
          className={`nav-btn ${currentPath === "/contact" ? "active" : ""}`}
        >
          Contact Us
        </button>

        {isAuthenticated && (
          <button
            onClick={() => navigate("/result")}
            className={`nav-btn ${currentPath === "/result" ? "active" : ""}`}
          >
            Results
          </button>
        )}

        {isAuthenticated ? (
          <>
            <button onClick={() => logout({ returnTo: window.location.origin })} className="auth-btn">
              Logout
            </button>
            <button onClick={handleDeleteAccount} className="nav-btn delete-btn">
              Delete Account
            </button>
          </>
        ) : (
          <>
            <button
              onClick={() =>
                loginWithRedirect({
                  authorizationParams: {
                    screen_hint: "signup",
                    redirect_uri: window.location.origin + "/form",
                  },
                })
              }
              className="auth-btn"
            >
              Sign Up
            </button>

            <button
              onClick={() =>
                loginWithRedirect({
                  authorizationParams: {
                    redirect_uri: window.location.origin + "/result",
                  },
                })
              }
              className="auth-btn"
            >
              Login
            </button>
          </>
        )}
      </nav>
    </header>
  );
}

export default Header;
