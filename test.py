import pyodbc 
import sys

#arg1 = sys.argv[1]
#arg2 = sys.argv[2]
#arg1 = 'NA1_4739460864'
#arg2 = 'RED'

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=DUOED;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
arg1 = 'NA1_4739460864'
arg2 = 'RED'

insert_query = "INSERT INTO DBO.Matches (matchID, matchResult) VALUES (?, ?)"

# Execute the query with the values
cursor.execute(insert_query, (arg1, arg2))

# Commit the transaction to persist the changes
conn.commit()

# SQL query to select all rows from a table
select_query = "SELECT * FROM DBO.Matches"

# Execute the query
cursor.execute(select_query)

# Fetch all the rows
rows = cursor.fetchall()

# Print the retrieved rows
for row in rows:
    print(row)

# Close the connection
conn.close()