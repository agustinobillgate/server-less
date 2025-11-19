const { connectToSchema } = require('./db');
const fs = require('fs');
const path = require('path');

async function run() {
  const schema = 'qcserverless3';  // bisa berubah kapan saja
  const client = await connectToSchema(schema);
  const result = await client.query("SELECT * FROM queasy WHERE key=$1 ORDER BY _recid", [171]);
  console.log(result.rows);

  const jsonOutput = JSON.stringify(result.rows, null, 2);
  const outputPath = path.join(__dirname, `queasy171_${schema}.json`);

  fs.writeFileSync(outputPath, jsonOutput, 'utf8');

  console.log(`💾 Saved to ${outputPath}`);
  await client.end();
}

run();
