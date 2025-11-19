// pg_test.js
require('dotenv').config();  // load .env

const { Client } = require('pg');

async function main() {
  const client = new Client({
    host:     process.env.DB_HOST,
    port:     process.env.DB_PORT,
    database: process.env.DB_NAME,
    user:     process.env.DB_USER,
    password: process.env.DB_PASSWORD,
  });

  let hotel_schema = "qcserverless3";
  let sql_select_schema = `SET search_path TO ${hotel_schema}`;
  let sql_170 = "SELECT COUNT(*) AS count_170 FROM queasy WHERE key=170";
  let sql_171 = "SELECT COUNT(*) AS count_171 FROM queasy WHERE key=171";
  let sql_schema_public = "SET search_path TO public";
  try {
    await client.connect();
    console.log("✅ Connected to PostgreSQL");
    await client.query(sql_select_schema);
    const result = await client.query("SELECT now() AS server_time");
    console.log("⏰ Server time:", result.rows[0].server_time);

    await client.query(sql_select_schema);
    const res_170 = await client.query(sql_170);
    console.log("🔢 Count for key=170:", res_170.rows[0].count_170);
    const res_171 = await client.query(sql_171);
    console.log("🔢 Count for key=171:", res_171.rows[0].count_171);

    await client.query(sql_schema_public);
    console.log("✅ Schema reset to public");
  } catch (err) {
    console.error("❌ Error connecting or querying:", err.message);
  } finally {
    await client.end();
    console.log("🔌 Connection closed");
  }
}

main();
