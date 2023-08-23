const sql = require('mssql');

const config = {
    server: 'localhost',        // Replace with your SQL Server hostname or IP address
    user: 'AsusROG\\epicf',
    database: 'DUOED',
    password: '~~~~',
    options: {
      trustedConnection: true,        // Use Windows authentication
      trustServerCertificate: true,   
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

  // Rest of your database operations here...

  // Close the connection pool when you're done
  pool.close();
  console.log('Connection to the database closed');
});
