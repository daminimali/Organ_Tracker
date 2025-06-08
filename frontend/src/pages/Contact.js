// src/components/Contact.js
import React from 'react';
import '../styles/Contact.css';

function Contact() {
  return (
    <section id="contact" className="contact">
      <h3>Contact Us</h3>
      <p>Interested in collaborating or have questions/suggestions? Reach out to us!🔥</p>
      <form className="contact-form">
        <input type="text" placeholder="Your Name" required />
        <input type="email" placeholder="Your Email" required />
        <textarea placeholder="Your Message" required></textarea>
        <button type="submit">Send Message</button>
      </form>
    </section>
  );
}

export default Contact;
