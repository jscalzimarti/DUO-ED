#pulling data from only solo queue in season 13 and entering it into the database - with print statements

from findMatchTimestamp import find_match_timestamp
from findMatchSeason import find_match_season
from findMatchQueue import find_match_queue

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

apiKey = 'RGAPI-da221bc0-65ee-4894-9b93-3b7653c963db'
region = 'na1'
summonerName = 'AYD Anarchy'
currentSeason = 13
currentQueue = 420
start = 0
count = 20

url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={apiKey}'
response = requests.get(url)
data = response.json()
puuid = data['puuid']

matchIds = "" # bugfix????
all_match_ids = []  # Initialize an empty list to store all matchIds

flag = False
for _ in range(50):
    url2 = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&api_key={apiKey}'
    response2 = requests.get(url2)
    matchIds = response2.json()

    # Extend the all_match_ids list with the matchIds from this iteration
    all_match_ids.extend(matchIds)
    
    # Increment start for the next iteration if you want to retrieve different data
    start += count
    if matchIds: # for testing only, switch to for statement for deployment
    #for matchId in matchIds:
        print(start)
        if (find_match_season(find_match_timestamp(matchIds[-1], apiKey))) != currentSeason:
            flag = True
            break
    if flag:
        break
        





counter = 0
counter2 = 0
matchInfo = []

def fetch_match_data(matchId):
    url3 = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={apiKey}'
    try:
        response3 = requests.get(url3)
        data3 = response3.json()
        
        matchInfo.append(matchId)
        
        teams = data3['info']['teams']
        for team in teams:
            if team['teamId'] == 100 and team['win']:
                matchInfo.append('BLUE')
            elif team['teamId'] == 200 and team['win']:
                matchInfo.append('RED')

        participants = data3['info']['participants']
        
        for participant in participants:
            summoner_name = participant['summonerName']
            matchInfo.append(summoner_name)

        global counter2
        counter2 += 1
        print(counter2)
        print(matchInfo)




        # Prepare an SQL query to insert data into a table
        match_insert_query = "INSERT INTO DBO.Matches (matchID, matchResult) VALUES (?, ?)"

        # Execute the query with the values
        cursor.execute(match_insert_query, (matchInfo[0], matchInfo[1]))

        # Prepare an SQL query to insert data into a table
        participants_insert_query = "INSERT INTO DBO.Participants (matchID, team, participant) VALUES (?, ?, ?)"
        
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

    except Exception as e:
        print(e)

time.sleep(120)
count2 = 5
for match_id in all_match_ids:
    if count2 % 100 == 0:
        count2 = 5
        time.sleep(120) #api rate limits

    if (find_match_queue(match_id, apiKey)) == currentQueue:
        fetch_match_data(match_id)
        count2 += 5



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
rows = rows + newline + cursor.fetchall()

# Print the retrieved rows
for row in rows:
    print(row)

# Close the cursor and the database connection
cursor.close()
conn.close()