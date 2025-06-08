import mysql from 'mysql2/promise'; 
import dotenv from 'dotenv';
dotenv.config();

const pool = mysql.createPool({
    host: process.env.MYSQL_HOST,
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD, 
    database: process.env.MYSQL_DATABASE
});

export async function fetchAllDonors() {
    try {
        const [rows] = await pool.query("SELECT * FROM donors");
        return rows;
    } catch (error) {
        console.error("Error fetching all donors:", error);
        return [];
    }
}

export async function fetchAllReceivers() {
    try {
        const [rows] = await pool.query("SELECT * FROM receivers");
        return rows;
    } catch (error) {
        console.error("Error fetching all receivers:", error);
        return [];
    }
}

export async function fetchDonorById(id) {
    try {
        const [rows] = await pool.query(`
            SELECT * 
            FROM donors
            WHERE donor_id = ?`, [id]);  
        return rows;
    } catch (error) {
        console.error(`Error fetching donor with ID ${id}:`, error);
        return null;
    }
}

export async function fetchReceiverById(id) {
    try {
        const [rows] = await pool.query(`
            SELECT * 
            FROM receivers
            WHERE receiver_id = ?`, [id]);  
        return rows;
    } catch (error) {
        console.error(`Error fetching receiver with ID ${id}:`, error);
        return null;
    }
}


export async function createDonor(
  Auth0_ID,
  Age,
  Blood_Type,
  Organ_Type,
  HLA_Typing,
  BMI,
  Organ_Size,
  Infection_Status,
  Geographic_Location,
  Health_Conditions,
  phone_number
) {
  const connection = await pool.getConnection();
  try {
    // 1. Get latest donor_id
    const [rows] = await connection.query("SELECT donor_id FROM donors ORDER BY donor_id DESC LIMIT 1");
    let Donor_ID;

    if (rows.length === 0) {
      Donor_ID = "D001";
    } else {
      const lastId = rows[0].donor_id;
      const num = parseInt(lastId.substring(1)) + 1;
      Donor_ID = "D" + num.toString().padStart(3, "0");
    }

    // 2. Insert new donor
    const insertQuery = `
      INSERT INTO donors (
        Donor_ID, Auth0_ID, Age, Blood_Type, Organ_Type, HLA_Typing, BMI, Organ_Size,
        Infection_status, Geographic_Location, Health_Conditions, phone_number
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const values = [
      Donor_ID,
      Auth0_ID,
      Age,
      Blood_Type,
      Organ_Type,
      HLA_Typing,
      BMI,
      Organ_Size,
      Infection_Status,
      Geographic_Location,
      Health_Conditions,
      phone_number
    ];

    await connection.query(insertQuery, values);
    return Donor_ID;

  } catch (err) {
    throw err;
  } finally {
    connection.release();
  }
}
  
export async function createReceiver(
  Auth0_ID,
  Age,
  Blood_Type,
  Organ_Type,
  HLA_Typing_Requirement,
  BMI,
  Infection_status,
  Urgency_Level,
  Waiting_Time,
  Geographic_Location,
  Health_Conditions,
  phone_number
) {
  const connection = await pool.getConnection();
  try {
    // 1. Get latest receiver_id
    const [rows] = await connection.query("SELECT Recipient_ID  FROM receivers ORDER BY Recipient_ID DESC LIMIT 1");
    let Recipient_ID ;

    if (rows.length === 0) {
      Recipient_ID  = "R001";
    } else {
      const lastId = rows[0].receiver_id;
      const num = parseInt(lastId.substring(1)) + 1;
      Recipient_ID  = "R" + num.toString().padStart(3, "0");
    }

    // 2. Insert new receiver
    const insertQuery = `
      INSERT INTO receivers (
        Recipient_ID, Auth0_ID, Age, Blood_Type, Organ_Type, HLA_Typing_Requirement, BMI,
        Infection_Status, Urgency_Level, Waiting_Time, Geographic_Location, Health_Conditions, phone_number
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const values = [
      Recipient_ID ,
      Auth0_ID,
      Age,
      Blood_Type,
      Organ_Type,
      HLA_Typing_Requirement,
      BMI,
      Infection_status,
      Urgency_Level,
      Waiting_Time,
      Geographic_Location,
      Health_Conditions,
      phone_number
    ];

    await connection.query(insertQuery, values);
    return Recipient_ID;

  } catch (err) {
    throw err;
  } finally {
    connection.release();
  }
}
  
export async function deleteUserByDonorId(donorId) {
    const [result] = await pool.query("DELETE FROM donors WHERE donor_id = ?", [donorId]);
    return result.affectedRows;
}

export async function deleteUserByReceiverId(receiverId) {
    const [result] = await pool.query("DELETE FROM receivers WHERE receiver_id = ?", [receiverId]);
    return result.affectedRows;
}
