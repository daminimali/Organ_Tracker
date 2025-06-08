// src/pages/Footer.js
import React from 'react';
import '../styles/Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">

        <div className="footer-section">
          <h4>Useful Links:</h4>
          <ul>
            <li>
              <a
                href="https://www.dkms-india.org/"
                target="_blank"
                rel="noopener noreferrer"
              >
                Know your HLA Typing for Free
              </a>
            </li>
            <li>
              <a
                href="https://www.mohfw.gov.in/"
                target="_blank"
                rel="noopener noreferrer"
              >
                Ministry of Health (India)
              </a>
            </li>
            <li>
              <a
                href="https://www.organindia.org/"
                target="_blank"
                rel="noopener noreferrer"
              >
                Organ Donation Awareness
              </a>
            </li>
            <li>
              <a
                href="https://www.who.int/health-topics/transplantation#tab=tab_1"
                target="_blank"
                rel="noopener noreferrer"
              >
                World Health Organization (W.H.O.)
              </a>
            </li>
            <li>
              <a
                href="https://github.com/SuyashMarathe/Organ-Tracker"
                target="_blank"
                rel="noopener noreferrer"
              >
                Source Code
              </a>
            </li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Disclaimer:</h4>
          <p>
          Organ Tracker does not guarantee a 100% success rate for organ transplants. The primary goal of this project is to enhance the probability of successful matches and to facilitate faster and more secure donor-recipient connections. While the likelihood of transplant failure after prediction is low, Organ Tracker cannot be held responsible for any loss of life or complications arising from unsuccessful organ transplants.
          </p>
        </div>
      </div>

      <div className="footer-bottom">
        <p>Copyright © 2025 All Rights Reserved | Organ Tracker</p>
      </div>
      <div className="footer-bottomlast">
      <p>Last Updated : 11-04-2025 | Version : 1.0.0 | Made on Earth by Humans.</p>
      </div>
    </footer>
  );
}

export default Footer;
