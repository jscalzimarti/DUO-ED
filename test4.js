/*const sqlQuery = `SELECT * FROM dbo.Matches`;

query(sqlQuery, (err, results) => {
    if (err) {
      console.error('Error executing SQL query:', err);
      res.status(500).json({ error: 'An error occurred while executing the query.' });
    } else {
      res.json(results);
    }
  });*/

  const fs = require('fs');
const mysql = require('mysql');

// Assuming you already have a connection object named 'connection' established and configured correctly.

const sqlFilePath = 'path/to/your/queries.sql';

// Read the SQL file content
const sqlFileContent = `SELECT * FROM dbo.Matches`;

// Split SQL queries by semicolon to execute them separately
const sqlQueries = sqlFileContent.split(';');

// Remove the last element of the array (it will be an empty string)
sqlQueries.pop();

// Run each SQL query one by one
sqlQueries.forEach((query) => {
  connection.query(query, (error, results, fields) => {
    if (error) {
      console.error('Error executing SQL query:', error);
    } else {
      console.log('Query executed successfully:', query);
      console.log('Results:', results);
    }
  });
});

// Close the MySQL connection after all queries are executed (optional, depending on your use case)
// connection.end();
