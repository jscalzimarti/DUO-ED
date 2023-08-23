const { Connection, Request } = require('tedious');

const config = {
  server: 'localhost',
  authentication: {
    type: 'default',
    options: {
        userName: 'AsusROG\\epicf', // Replace with your Windows username (domain\\username)
        password: '~~~~~', // Replace with your Windows password
    },
  },
  options: {
    database: 'master', // Replace with your database name
    trustServerCertificate: true,
  },
};

// Create a connection to the database
const connection = new Connection(config);

// Event handler for when the connection is established
connection.on('connect', (err) => {
  if (err) {
    console.error('Error connecting to the database: ', err.message);
    return;
  }

  console.log('Connected to the database');

  // Execute a SQL query
  executeQuery();
});

// Event handler for when an error occurs during the connection
connection.on('error', (err) => {
  console.error('Database connection error: ', err.message);
});

// Function to execute a SQL query
function executeQuery() {
  // Replace the SQL query with your desired query
  const query = 'SELECT * FROM dbo.Matches';

  // Create a new Request object
  const request = new Request(query, (err, rowCount, rows) => {
    if (err) {
      console.error('Error executing the query: ', err.message);
      return;
    }

    // Log the query result
    console.log('Query Result:', rows);

    // Close the database connection
    connection.close();
  });

  // Event handler for when a row is received
  request.on('row', (columns) => {
    // Log each column value for the row
    columns.forEach((column) => {
      console.log(column.value);
    });
  });

  // Execute the request
  connection.execSql(request);
}

// Connect to the database
connection.connect();
