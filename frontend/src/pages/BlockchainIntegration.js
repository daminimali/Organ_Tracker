import React, { useEffect } from "react";
import "../styles/BlockchainIntegration.css";
import blockchainImage from "../images/blockchain-image.jpg";

function BlockchainIntegration() {
  useEffect(() => {
    const handleScroll = () => {
      const blockchainSection = document.getElementById("blockchain");
      if (!blockchainSection) return;

      const blockchainContent = document.querySelector(".blockchain-content");
      const blockchainImage = document.querySelector(".blockchain-image");

      const rect = blockchainSection.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom >= 0) {
        blockchainContent?.classList.add("slide-in-right");
        blockchainImage?.classList.add("slide-in-left");
      } else {
        blockchainContent?.classList.remove("slide-in-right");
        blockchainImage?.classList.remove("slide-in-left");
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <section id="blockchain" className="blockchain">
      <div className="blockchain-content">
        <h3>Blockchain for Secure Tracking</h3>
        <p>Blockchain provides a secure, transparent, and immutable ledger for tracking organ donations from donor to recipient.</p>
      </div>
      <div className="blockchain-image-container">
        <img src={blockchainImage} alt="Blockchain Tracking" className="blockchain-image" />
      </div>
    </section>
  );
}

export default BlockchainIntegration;
