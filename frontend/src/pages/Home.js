// src/Home.js
import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

function Home() {
  const navigate = useNavigate();
  const { loginWithRedirect, isAuthenticated } = useAuth0();

  return (
    <div className="home-container">
      <h2>Welcome to Organ Tracker!!</h2>
      <p>Track and manage organ donations with ease.</p>

      <div className={`home-btn-group ${isAuthenticated ? 'single-button' : ''}`}>
        <button className="home-btn" onClick={() => navigate('/about')}>
          Learn More
        </button>

        {!isAuthenticated && (
          <button
            className="home-btn"
            onClick={() =>
              loginWithRedirect({
                authorizationParams: {
                  screen_hint: 'signup',
                  redirect_uri: window.location.origin + '/form',
                },
              })
            }
          >
            Get Started
          </button>
        )}
      </div>
    </div>
  );
}

export default Home;
