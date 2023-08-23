// app.js (your main server file)

const express = require('express');
const mysql = require('mysql');

const app = express();

// MySQL configuration
const connection = mysql.createConnection({
  host: 'localhost',
  //user: 'your-mysql-user',
  //password: 'your-mysql-password',
  database: 'DUOED',
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    return;
  }
  console.log('Connected to MySQL database.');
});

// API endpoint to execute the SQL query
app.get('/api/query', (req, res) => {
  const { parameter1, parameter2 } = req.query;
  
  // Replace the following SQL query with your own query logic
  const sqlQuery = `SELECT * FROM dbo.Matches`;

  connection.query(sqlQuery, (err, results) => {
    if (err) {
      console.error('Error executing SQL query:', err);
      res.status(500).json({ error: 'An error occurred while executing the query.' });
    } else {
      res.json(results);
    }
  });
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
