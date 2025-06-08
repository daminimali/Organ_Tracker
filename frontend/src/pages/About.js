import React, { useEffect } from "react";
import "../styles/About.css";
import aboutImage from "../images/organ-donation-day.jpg";
import CompatibilityCheck from "./CompatibilityCheck.js";
import BlockchainIntegration from "./BlockchainIntegration.js";

function About() {
  useEffect(() => {
    setTimeout(() => {
      const aboutContent = document.querySelector(".about-content");
      const aboutImage = document.querySelector(".about-image");
      aboutContent?.classList.add("slide-in-right");
      aboutImage?.classList.add("slide-in-left");
    }, 100);
  }, []);

  return (
    <>
      {/* About Organ Tracker Section */}
      <section id="about" className="about">
        <div className="about-content">
          <h3>About Organ Tracker</h3>
          <p>Organ Tracker ensures a secure and transparent organ donation process using blockchain and AI.</p>
        </div>
        <div className="about-image-container">
          <img src={aboutImage} alt="Organ Donation" className="about-image" />
        </div>
      </section>

      {/* Organ Compatibility Section */}
      <CompatibilityCheck />

      {/* Blockchain for Secure Tracking Section */}
      <BlockchainIntegration />
    </>
  );
}

export default About;
