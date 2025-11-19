// db.js
require("dotenv").config();
const { Client } = require("pg");

const DB_CONFIG = {
  host:     process.env.DB_HOST,
  port:     process.env.DB_PORT,
  database: process.env.DB_NAME,
  user:     process.env.DB_USER,
  password: process.env.DB_PASS,
};

/**
 * connectToSchema(schemaName)
 *  - buka koneksi ke DB
 *  - switch schema sesuai variable schemaName
 *  - return client (siap untuk query)
 */
async function connectToSchema(schemaName) {
  if (!schemaName) {
    throw new Error("schemaName harus diisi");
  }

  // validasi basic agar aman dari injection
  if (!/^[a-zA-Z0-9_]+$/.test(schemaName)) {
    throw new Error(`Invalid schema name: ${schemaName}`);
  }

  const client = new Client(DB_CONFIG);
  await client.connect();

  // SET search_path ke schema yang dipilih
  await client.query(`SET search_path TO "${schemaName}"`);

  return client;
}

module.exports = {
  connectToSchema,
};
