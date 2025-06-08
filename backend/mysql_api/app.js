//app.js
// Import dependencies
const express = require("express");
const cors = require("cors");

// Import your custom functions (adjust the path if needed)
const { createDonor, createReceiver } = require("./database"); 

// Initialize express app
const app = express();
app.use(cors());
app.use(express.json());

// Create donor
app.post("/donors", async (req, res) => {
  const {
    auth0Id,
    age,
    blood_group,
    organ_type,
    hla_typing,
    bmi,
    organ_size,
    infection_status,
    location,
    health_condition,
    phone_number
  } = req.body;

  if (!auth0Id) {
    return res.status(400).json({ error: "auth0Id is required" });
  }

  try {
    const donor = await createDonor(
      auth0Id,
      age,
      blood_group,
      organ_type,
      hla_typing,
      bmi,
      organ_size,
      infection_status,
      location,
      health_condition,
      phone_number
    );

    res.status(201).send({ message: "Donor Created Successfully", id: donor });
  } catch (error) {
    console.error("Error creating donor:", error);
    res.status(500).send({ error: "Failed to create donor" });
  }
});

// Create receiver
app.post("/receivers", async (req, res) => {
  const {
    auth0Id,
    age,
    blood_group,
    organ_type,
    hla_typing,
    bmi,
    infection_status,
    urgency,
    waiting_time,
    location,
    health_condition,
    phone_number
  } = req.body;

  if (!auth0Id) {
    return res.status(400).json({ error: "auth0Id is required" });
  }

  try {
    const receiver = await createReceiver(
      auth0Id,
      age,
      blood_group,
      organ_type,
      hla_typing,
      bmi,
      infection_status,
      urgency,
      waiting_time,
      location,
      health_condition,
      phone_number
    );

    res.status(201).send({ message: "Receiver Created Successfully", id: receiver });
  } catch (error) {
    console.error("Error creating receiver:", error);
    res.status(500).send({ error: "Failed to create receiver" });
  }
});

// Start server
const PORT = 3001;
app.listen(PORT, () => {
  console.log(`🚀 Server is running on http://localhost:${PORT}`);
});
