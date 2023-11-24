#    Function to preview the content of the Matches and Participants tables in the DUOED database.
#
#    Returns:
#    None

import pyodbc

def preview_database():

    # Establish a connection to the database
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=DUOED;'
                      'Trusted_Connection=yes;')

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # SQL query to select all rows from a table
    matches_select_query = "SELECT * FROM DBO.Matches"

    # Execute the query
    cursor.execute(matches_select_query)

    # Fetch all the rows
    rows = cursor.fetchall()

    # SQL query to select all rows from a table
    participants_select_query = "SELECT * FROM DBO.Participants"

    # Execute the query
    cursor.execute(participants_select_query)

    # Fetch all the rows while combining the output of both select statements
    newline = ["\n"]
    rows = newline + newline + rows + newline + cursor.fetchall()

    # Print the retrieved rows
    for row in rows:               #commented out for testing
        print(row)                 #commented out for testing

    # Close the cursor and the database connection
    cursor.close()
    conn.close()