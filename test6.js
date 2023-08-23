const sql = require('mssql');

const config = {
    server: 'localhost',
    user: 'ASUSROG/epicf',
    password: '~~~~',
    database: 'DUOED',
  options: {
    trustedConnection: true,   // Use Windows authentication
  },
};

// Create a connection pool
const pool = new sql.ConnectionPool(config);

// Connect to the database
pool.connect((err) => {
  if (err) {
    console.error('Error connecting to the database: ', err);
    return;
  }

  console.log('Connected to the database');

  // Create a new SQL query
  const query = 'SELECT * FROM dbo.Matches';

  // Execute the query
  pool.request().query(query, (err, result) => {
    if (err) {
      console.error('Error executing the query: ', err);
      return;
    }

    // Log the results
    console.log('Query Results:', result.recordset);

    // Close the connection pool
    pool.close((err) => {
      if (err) {
        console.error('Error closing the database connection: ', err);
        return;
      }
      console.log('Connection to the database closed');
    });
  });
});
