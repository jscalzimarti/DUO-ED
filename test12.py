#pulling data from only solo queue in season 13 and entering it into the database - with print statements

from findMatchTimestamp import find_match_timestamp
from findMatchSeason import find_match_season
from findMatchQueue import find_match_queue
from fetchMatchData import fetch_match_data

import requests
import pyodbc
import time

# Establish a connection to the database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=DUOED;'
                      'Trusted_Connection=yes;')

# Create a cursor to interact with the database
cursor = conn.cursor()

apiKey = 'RGAPI-1cdc4dcb-53ca-40e2-b844-c97e67be8c85'
region = 'na1'
summonerName = 'AYD Anarchy'
participant1 = summonerName
participant2 = 'AYD Trash'
currentSeason = 13
currentQueue = 420
matchIdStart = 0
matchIdsCount = 20

url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={apiKey}'
response = requests.get(url)
data = response.json()
puuid = data['puuid']

matchIds = "" # bugfix????
all_match_ids = []  # Initialize an empty list to store all matchIds

current_season_flag = True
count3 = 0
for _ in range(50):
    url2 = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={matchIdStart}&count={matchIdsCount}&api_key={apiKey}'
    response2 = requests.get(url2)
    matchIds = response2.json()

    # Extend the all_match_ids list with the matchIds from this iteration
    
    
    # Increment start for the next iteration if you want to retrieve different data
    matchIdStart += matchIdsCount
    #if matchIds: # for testing only, switch to for statement for deployment
    for matchId in matchIds:
        count3 += 1
        if count3 % 30 == 0:
            time.sleep(60)

        if (find_match_queue(matchId, apiKey)) == currentQueue:
            print(count3)
            all_match_ids.append(matchId)
            

        #if (find_match_season(find_match_timestamp(matchIds[-1], apiKey))) != currentSeason:
        if (find_match_season(find_match_timestamp(matchId, apiKey))) != currentSeason:
            current_season_flag = False
            break
    if current_season_flag != True:
        break
        


match_id_counter = 0
for match_id in all_match_ids:
    print(match_id)
    match_id_counter += 1
print(match_id_counter)


time.sleep(120)
api_call_counter = 0
for match_id in all_match_ids:
    if api_call_counter != 0:
        if api_call_counter % 120 == 0:
            api_call_counter = 0
            time.sleep(120) #api rate limits

    matchInfo = fetch_match_data(match_id, apiKey)
    api_call_counter += 1


    # Prepare an SQL query to insert data into a table
    try:
        match_insert_query = "INSERT INTO DBO.Matches (matchID, matchResult) VALUES (?, ?)"
    except Exception as e:
        print(e)

    # Execute the query with the values
    cursor.execute(match_insert_query, (matchInfo[0], matchInfo[1]))

    # Prepare an SQL query to insert data into a table
    try:
        participants_insert_query = "INSERT INTO DBO.Participants (matchID, team, participant) VALUES (?, ?, ?)"
    except Exception as e:
        print(e)
    
    i = 2
    while i >= 2 and i < len(matchInfo):
        if i < 7:
            team = 'BLUE'
        else:
            team = 'RED'

        # Execute the query with the values
        cursor.execute(participants_insert_query, (matchInfo[0], team, matchInfo[i]))
        i += 1

    matchInfo.clear()
    time.sleep(1)



# Commit the transaction to persist the changes
conn.commit()

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
row_count = 0
for row in rows:
    print(row)
    row_count += 1
    if row_count == 25:
        time.sleep(3)




# SQL query to find number of matches participant1 played in the selected queue
cursor.execute('''
    select m.*
    from dbo.Matches m
    inner join Participants p on m.matchID = p.matchID
    where p.participant = ?
''', participant1)

# Fetch the results
matches_1 = cursor.fetchall()

# SQL query 2
cursor.execute('''
    select * 
    from dbo.Participants
    where matchID in (select matchID from dbo.Participants where participant = ?)
    order by matchID ASC;
''', participant1)

matches_2 = cursor.fetchall()

# SQL query 3
cursor.execute('''
    SELECT m.*
    FROM dbo.Matches m
    INNER JOIN Participants p1 ON m.matchID = p1.matchID AND p1.participant = ?
    INNER JOIN Participants p2 ON m.matchID = p2.matchID AND p2.participant = ?
    ORDER BY matchID ASC;
''', participant1, participant2)

matches_3 = cursor.fetchall()

# SQL query 4
cursor.execute('''
    SELECT p.*
    FROM dbo.Participants p
    INNER JOIN (SELECT DISTINCT matchID FROM dbo.Participants WHERE participant = ?) p1 ON p.matchID = p1.matchID
    INNER JOIN (SELECT DISTINCT matchID FROM dbo.Participants WHERE participant = ?) p2 ON p.matchID = p2.matchID
    ORDER BY p.matchID ASC;
''', participant1, participant2)

matches_4 = cursor.fetchall()

# SQL query 5
cursor.execute('''
    select p1.matchID, p1.participant as participant1, p2.participant as participant2
    from Participants p1
    inner join Participants p2 on p1.matchID = p2.matchID
    where p1.participant = ? and p2.participant = ? and p1.team = p2.team;
''', participant1, participant2)

matches_5 = cursor.fetchall()

# SQL query 6
cursor.execute('''
    SELECT p1.matchID, p1.participant AS participant1, p2.participant AS participant2
    FROM Participants p1
    INNER JOIN Participants p2 ON p1.matchID = p2.matchID
    INNER JOIN Matches m ON p1.matchID = m.matchID
    WHERE p1.participant = ? 
        AND p2.participant = ? 
        AND p1.team = p2.team
        AND p1.team = m.matchresult;
''', participant1, participant2)

matches_6 = cursor.fetchall()


# Output the results

print(f'Number of matches {participant1} played in the selected queue: {len(matches_1)}')
print(f'Number of matches {participant1} played with {participant2} in the selected queue: {len(matches_3)}')
print(f'Number of matches {participant1} played on the same team with {participant2} in the selected queue: {len(matches_5)}')
print(f'Number of matches {participant1} played on the same team with {participant2} and won in the selected queue: {len(matches_6)}')
print(f'When playing togeather in the selected queue {participant1} and {participant2} have a {round(len(matches_6)/len(matches_5), 2)}% winrate togeather')

# Close the cursor and the database connection
cursor.close()
conn.close()