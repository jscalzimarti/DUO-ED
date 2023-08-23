// Import required modules
const mysql = require('mysql');

// Create a connection to the database
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'ASUSROG/epicf',
    password: '~~~~',
    database: 'DUOED',
});

// Your function that returns a list of values
/*function getValues() {
  // Your logic to get the values
  const values = ['value1', 'value2', 'value3'];
  return values;
}*/

// Connect to the database
connection.connect((err) => {
  if (err) {
    console.error('Error connecting to the database: ', err);
    return;
  }

  console.log('Connected to the database');

  // Get the list of values
/* const valuesList = getValues();*/

  // Save each value to the database
  valuesList.forEach((value) => {
    connection.query(`SELECT * FROM dbo.Matches`);
  });

  // Close the connection
  connection.end((err) => {
    if (err) {
      console.error('Error closing the database connection: ', err);
      return;
    }
    console.log('Connection to the database closed');
  });
});
