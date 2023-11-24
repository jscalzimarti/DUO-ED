#   Function to make API calls to Riot Games API, retrieve match data, and store it in a SQL Server database.
#
#    Parameters:
#    participants (list): List of summoner names.
#    #region (str): Region code for the Riot Games API (e.g., 'na', 'euw').
#    apiKey (str): Riot Games API key.
#
#    Returns:
#    None

import requests
import pyodbc
import time

from findSeasonEpochTime import find_season_epoch_time
from fetchMatchData6 import fetch_match_data

def api_calls(participants, region, apiKey):    #participants is a list passed by the website
                                                #however it can also just be a single value FOR THIS CODE ONLY

    # Establish a connection to the database
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=DUOED;'
                      'Trusted_Connection=yes;')

    # Create a cursor to interact with the database
    cursor = conn.cursor()


    matchIdStart = 0 # Match ID start location
    matchIdsCount = 20 # Match ID's queried per each rotation of the for loop
    summonerName = participants[0] # Main summonerName to be queried and added to the database


    #Queue and Season should be an arguement passed by the website
    currentSeason = 13  #code currently cannot do previous seasons prior to season 12
    currentQueue = 420  #code can accept multiple queues as an arguement (syntax: 0, 420, 700) 

    # Construct the summoner URL to get summoner puuid
    # puuid is used in the Riot Games match v5 API
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={apiKey}'

    # Make the API call to get summoner puuid
    response = requests.get(url)
    data = response.json()
    puuid = data['puuid']

    matchIds = ""
    all_match_ids = []  # Initialize an empty list to store all matchIds

    # Find the epoch start and end time for the current season
    # epoch start and end time are used in the Riot Games match v5 API
    seasonStartTime, seasonEndTime = find_season_epoch_time(currentSeason)

    for _ in range(1):
        if isinstance(currentQueue, int):
            # Construct the match v5 URL for a single queue
            url2 = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={seasonStartTime}&endTime={seasonEndTime}&queue={currentQueue}&start={matchIdStart}&count={matchIdsCount}&api_key={apiKey}'
        else:
            # Construct the match v5 URL for multiple queues
            for queue in currentQueue:
                url2 = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={seasonStartTime}&endTime={seasonEndTime}&queue={queue}&start={matchIdStart}&count={matchIdsCount}&api_key={apiKey}'
        
        # Running the API call to get match IDs
        response2 = requests.get(url2)
        matchIds = response2.json()      
        
        # Increment start for the next iteration if you want to retrieve different data
        matchIdStart += matchIdsCount
        for matchId in matchIds:
            all_match_ids.append(matchId)

    
    api_call_counter = 0
    for match_id in all_match_ids:

        #api rate limits
        if api_call_counter != 0:
            if api_call_counter % 80 == 0:
                api_call_counter = 0
                time.sleep(120) #api rate limits

        matchInfo = fetch_match_data(match_id, apiKey)
        api_call_counter += 1



        # Prepare an SQL query to insert data into a table for matches
        try:
            match_insert_query = "INSERT INTO DBO.Matches (matchID, matchResult, matchQueue, matchDuration) VALUES (?, ?, ?, ?)"
        except Exception as e:
            print(e)

        # Execute the query with the values for matches
        try:
            cursor.execute(match_insert_query, (matchInfo[0], matchInfo[1], matchInfo[2], matchInfo[3]))
        except Exception as e:
            print(e)

        # Prepare an SQL query to insert data into a table for participants
        try:
            participants_insert_query = "INSERT INTO DBO.Participants (matchID, teamID, summonerName, teamPosition, championName, kda, kills, deaths, assists, killParticipation, physicalDamageDealtToChampions, magicDamageDealtToChampions, trueDamageDealtToChampions, totalDamageDealtToChampions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        except Exception as e:
            print(e)
        
        # Iterate through the matchInfo list starting from index 4 to process participant data
        i = 4
        try:
            while i >= 3 and i < len(matchInfo):
                # Determine the team based participant order in matchInfo list
                if matchInfo[i][1] == 100:
                    team = 'BLUE'
                else:
                    team = 'RED'

                # Execute the query with the values for participants
                cursor.execute(participants_insert_query, (matchInfo[0], team, matchInfo[i][0], matchInfo[i][2], matchInfo[i][3], matchInfo[i][4], matchInfo[i][5], matchInfo[i][6], matchInfo[i][7], matchInfo[i][8], matchInfo[i][9], matchInfo[i][10], matchInfo[i][11], matchInfo[i][12]))
                i += 1
            
            matchInfo.clear()
        except Exception as e:
            print(e)

    # Commit the transaction to persist the changes
    conn.commit()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()