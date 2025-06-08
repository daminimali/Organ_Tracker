// src/components/FormPage.js
import React, { useState } from "react";
import axios from "axios";
import "../styles/FormPage.css";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from "react-router-dom";

function FormPage() {
  const { user, isAuthenticated, isLoading } = useAuth0();
  const [userType, setUserType] = useState(""); // "donor" or "receiver"
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    age: "",
    blood_type: "",
    organ_type: "",
    hla_typing: "",
    bmi: "",
    organ_size: "",
    infection_status: "",
    urgency_level: "",
    waiting_time: "",
    geographic_location: "",
    health_conditions: "",
    phone_number: ""
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isAuthenticated || !user || isLoading) {
      alert("Please log in to register.");
      return;
    }

    try {
      const auth0Id = user.sub;

      // Express server URLs on port 3001
      const endpoint =
        userType === "donor"
          ? "http://localhost:3001/donors"
          : "http://localhost:3001/receivers";

      const payload = {
        auth0Id,
        name: user.name || "Anonymous",
        age: formData.age,
        blood_group: formData.blood_type,
        organ_type: formData.organ_type,
        hla_typing: formData.hla_typing,
        bmi: formData.bmi,
        organ_size: formData.organ_size,
        infection_status: formData.infection_status,
        location: formData.geographic_location,
        health_condition: formData.health_conditions,
        phone_number: formData.phone_number,
        urgency: formData.urgency_level,
        waiting_time: formData.waiting_time
      };

      await axios.post(endpoint, payload);
      alert(`${userType === "donor" ? "Donor" : "Receiver"} Registered Successfully!`);
      navigate("/result"); // Redirect to ResultPage
    } catch (error) {
      console.error(`Error submitting ${userType} data:`, error);
      alert("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="form-container">
      <h2>Register as a Donor or Recipient</h2>

      <div className="user-selection">
        <button
          className={userType === "donor" ? "active" : ""}
          onClick={() => setUserType("donor")}
        >
          Register as Donor
        </button>
        <button
          className={userType === "receiver" ? "active" : ""}
          onClick={() => setUserType("receiver")}
        >
          Register as Receiver
        </button>
      </div>

      {userType && (
        <form className="user-form" onSubmit={handleSubmit}>
          <input type="number" name="age" placeholder="Age" onChange={handleChange} required />
          <input type="text" name="blood_type" placeholder="Blood Type" onChange={handleChange} required />
          <input type="text" name="organ_type" placeholder="Organ Type" onChange={handleChange} required />
          <input type="text" name="hla_typing" placeholder="HLA Typing" onChange={handleChange} required />
          <input type="number" name="bmi" placeholder="BMI" step="0.1" onChange={handleChange} required />

          {userType === "donor" && (
            <>
              <input type="number" name="organ_size" placeholder="Organ Size" step="0.1" onChange={handleChange} required />
              <input type="text" name="infection_status" placeholder="Infection Status" onChange={handleChange} />
              <input type="text" name="geographic_location" placeholder="Geographic Location" onChange={handleChange} required />
              <input type="text" name="health_conditions" placeholder="Health Conditions" onChange={handleChange} required />
            </>
          )}

          {userType === "receiver" && (
            <>
              <input type="text" name="infection_status" placeholder="Infection Status" onChange={handleChange} />
              <select name="urgency_level" onChange={handleChange} required>
                <option value="">Select Urgency</option>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
              <input
                type="number"
                name="waiting_time"
                placeholder="Waiting Time (in days)"
                onChange={handleChange}
                required
              />
              <input type="text" name="geographic_location" placeholder="Geographic Location" onChange={handleChange} required />
              <input type="text" name="health_conditions" placeholder="Health Conditions" onChange={handleChange} required />
            </>
          )}

          <input type="tel" name="phone_number" placeholder="Phone Number" onChange={handleChange} required />

          <button type="submit" className="submit-btn">
            Register {userType === "donor" ? "Donor" : "Receiver"}
          </button>
        </form>
      )}
    </div>
  );
}

export default FormPage;
