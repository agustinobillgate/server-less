const { connectToSchema } = require('./db');

async function run() {
  const schema = 'qcserverless3';  // bisa berubah kapan saja
  const client = await connectToSchema(schema);
  const result = await client.query("SELECT * FROM queasy WHERE key=$1 ORDER BY _recid", [170]);
  console.log(result.rows);

  await client.end();
}

run();
