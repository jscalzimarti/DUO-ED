const sql = require('mssql');

// Database configuration
const config = {
    server: 'localhost',        // Replace with your SQL Server hostname or IP address
    user: 'ASUSROG/epicf',
    password: '~~~~',
    database: 'DUOED',
    options: {
      trustedConnection: true,   // Use Windows authentication
    },
  };

async function main() {
  try {
    // Create a connection pool
    const pool = await sql.connect(config);

    console.log('Connected to the database');

    // Sample data to be inserted into the database
    const dataToInsert = [
      { name: 'John Doe', age: 30 },
      { name: 'Jane Smith', age: 25 },
    ];

    // SQL query to insert data into the database
    const query = 'INSERT INTO dbo.Matches (Name, Age) VALUES (@name, @age)';

    // Prepare the SQL query and bind parameters
    const ps = new sql.PreparedStatement(pool);
    ps.input('name', sql.VarChar(50));
    ps.input('age', sql.Int);

    // Start a transaction (optional)
    const transaction = new sql.Transaction(pool);
    await transaction.begin();

    try {
      for (const row of dataToInsert) {
        await ps.prepare(query);
        await ps.execute(row);
        await ps.unprepare();
      }

      // Commit the transaction (optional)
      await transaction.commit();
      console.log('Data inserted successfully');
    } catch (err) {
      // Rollback the transaction in case of an error (optional)
      await transaction.rollback();
      throw err;
    } finally {
      // Close the connection pool
      await ps.unprepare();
      await pool.close();
      console.log('Connection to the database closed');
    }
  } catch (err) {
    console.error('Error:', err);
  }
}

// Call the main function
main();
