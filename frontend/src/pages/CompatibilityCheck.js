import React, { useEffect } from "react";
import "../styles/CompatibilityCheck.css";
import compatibilityImage from "../images/compatibility-image.jpg";

function CompatibilityCheck() {
  useEffect(() => {
    const handleScroll = () => {
      const compatibilitySection = document.getElementById("compatibility");
      if (!compatibilitySection) return;

      const compatibilityContent = document.querySelector(".compatibility-content");
      const compatibilityImage = document.querySelector(".compatibility-image");

      const rect = compatibilitySection.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom >= 0) {
        compatibilityContent?.classList.add("slide-in-left");
        compatibilityImage?.classList.add("slide-in-right");
      } else {
        compatibilityContent?.classList.remove("slide-in-left");
        compatibilityImage?.classList.remove("slide-in-right");
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <section id="compatibility" className="compatibility">
      <div className="compatibility-image-container">
        <img src={compatibilityImage} alt="Compatibility Check" className="compatibility-image" />
      </div>
      <div className="compatibility-content">
        <h3>Organ Compatibility Check</h3>
        <p>Our machine learning algorithms ensure that each organ matches the recipient’s medical criteria for a higher chance of transplant success.</p>
      </div>
    </section>
  );
}

export default CompatibilityCheck;
