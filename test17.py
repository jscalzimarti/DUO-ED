#pulling data from only solo queue in season 13 and entering it into the database - with print statements
#omitting the extraneous api calls
#this only works for matches played after June 16th, 2021
#use fetchMatchSeason for matches played before that date
#also added functionality for multiple queues to be queried

#added flag for updating database or not
updateFlag = True

#added flag for calling api calls or not
apiFlag = True

#added flag for viewing the current data in the database
previewFlag = True

#added flag for querying the database and running the functions to calculate the stats
queryFlag = True

#clean up these exception calls?

#adding new values to the database with fetchMatchData6


from findSeasonEpochTime import find_season_epoch_time
from fetchMatchData6 import fetch_match_data

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

apiKey = 'RGAPI-013205c4-5b24-4e61-aad8-713ea0b59730'
region = 'na1'
participants = 'AYD Trash', 'AYD Anarchy'
summonerName = participants[0]
participant1 = participants[0]
participant2 = participants[1]
currentSeason = 13 #code currently cannot do previous seasons prior to season 12
currentQueue = 420 #code can now accept multiple queues as an arguement (syntax: 0, 420, 700)

def api_calls(summonerName, region, apiKey):
    matchIdStart = 0
    matchIdsCount = 20

    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={apiKey}'

    response = requests.get(url)
    data = response.json()
    puuid = data['puuid']

    matchIds = "" # bugfix????
    all_match_ids = []  # Initialize an empty list to store all matchIds

    seasonStartTime, seasonEndTime = find_season_epoch_time(currentSeason)

    count3 = 0
    for _ in range(1):
        if isinstance(currentQueue, int):
            #queue = "queue"
            url2 = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={seasonStartTime}&endTime={seasonEndTime}&queue={currentQueue}&start={matchIdStart}&count={matchIdsCount}&api_key={apiKey}'
        else:
            #queue = "queues"
            for queue in currentQueue:
                url2 = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={seasonStartTime}&endTime={seasonEndTime}&queue={queue}&start={matchIdStart}&count={matchIdsCount}&api_key={apiKey}'
        
        #url2 = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={seasonStartTime}&endTime={seasonEndTime}&{queue}={",".join(map(str, currentQueue))}&start={matchIdStart}&count={matchIdsCount}&api_key={apiKey}'
        response2 = requests.get(url2)
        matchIds = response2.json()

        # Extend the all_match_ids list with the matchIds from this iteration
        
        
        # Increment start for the next iteration if you want to retrieve different data
        matchIdStart += matchIdsCount
        #if matchIds: # for testing only, switch to for statement for deployment
        for matchId in matchIds:
            count3 += 1
            #if count3 % 30 == 0:
                #time.sleep(60)

            print(count3)
            all_match_ids.append(matchId)


    match_id_counter = 0
    for match_id in all_match_ids:
        print(match_id)
        match_id_counter += 1
    print(match_id_counter)



    #time.sleep(120) #api rate limits
    api_call_counter = 0
    for match_id in all_match_ids:
        if api_call_counter != 0:
            if api_call_counter % 120 == 0:
                api_call_counter = 0
                #time.sleep(120) #api rate limits

        matchInfo = fetch_match_data(match_id, apiKey)
        api_call_counter += 1



        # Prepare an SQL query to insert data into a table
        try:
            match_insert_query = "INSERT INTO DBO.Matches (matchID, matchResult, matchQueue, matchDuration) VALUES (?, ?, ?, ?)"
        except Exception as e:
            print(e)


        # Execute the query with the values
        try:
            cursor.execute(match_insert_query, (matchInfo[0], matchInfo[1], matchInfo[2], matchInfo[3]))
        except Exception as e:
            print(e)

        # Prepare an SQL query to insert data into a table
        try:
            participants_insert_query = "INSERT INTO DBO.Participants (matchID, teamID, summonerName, teamPosition, championName, kda, kills, deaths, assists, killParticipation, physicalDamageDealtToChampions, magicDamageDealtToChampions, trueDamageDealtToChampions, totalDamageDealtToChampions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        except Exception as e:
            print(e)
        
        i = 4
        while i >= 3 and i < len(matchInfo):
            if matchInfo[i][1] == 100:
                team = 'BLUE'
            else:
                team = 'RED'

            # Execute the query with the values
            cursor.execute(participants_insert_query, (matchInfo[0], team, matchInfo[i][0], matchInfo[i][2], matchInfo[i][3], matchInfo[i][4], matchInfo[i][5], matchInfo[i][6], matchInfo[i][7], matchInfo[i][8], matchInfo[i][9], matchInfo[i][10], matchInfo[i][11], matchInfo[i][12]))
            i += 1

        matchInfo.clear()



    # Commit the transaction to persist the changes
    if updateFlag:
        conn.commit()

def preview_database():
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
    for row in rows:
        print(row)

def query_database():
    # SQL query to find number of matches participant1 played in the selected queue
    cursor.execute('''
        select m.*
        from dbo.Matches m
        inner join Participants p on m.matchID = p.matchID
        where p.summonerName = ?
    ''', participant1)

    # Fetch the results
    matches_1 = cursor.fetchall()

    # SQL query 2
    cursor.execute('''
        select * 
        from dbo.Participants
        where matchID in (select matchID from dbo.Participants where summonerName = ?)
        order by matchID ASC;
    ''', participant1)

    matches_2 = cursor.fetchall()

    # SQL query 3
    cursor.execute('''
        SELECT m.*
        FROM dbo.Matches m
        INNER JOIN Participants p1 ON m.matchID = p1.matchID AND p1.summonerName = ?
        INNER JOIN Participants p2 ON m.matchID = p2.matchID AND p2.summonerName = ?
        ORDER BY matchID ASC;
    ''', participant1, participant2)

    matches_3 = cursor.fetchall()

    # SQL query 4
    cursor.execute('''
        SELECT p.*
        FROM dbo.Participants p
        INNER JOIN (SELECT DISTINCT matchID FROM dbo.Participants WHERE summonerName = ?) p1 ON p.matchID = p1.matchID
        INNER JOIN (SELECT DISTINCT matchID FROM dbo.Participants WHERE summonerName = ?) p2 ON p.matchID = p2.matchID
        ORDER BY p.matchID ASC;
    ''', participant1, participant2)

    matches_4 = cursor.fetchall()

    # SQL query 5
    cursor.execute('''
        select p1.matchID, p1.summonerName as participant1, p2.summonerName as participant2
        from Participants p1
        inner join Participants p2 on p1.matchID = p2.matchID
        where p1.summonerName = ? and p2.summonerName = ? and p1.teamID = p2.teamID;
    ''', participant1, participant2)

    matches_5 = cursor.fetchall()

    # SQL query 6
    cursor.execute('''
        SELECT p1.matchID, p1.summonerName AS participant1, p2.summonerName AS participant2
        FROM Participants p1
        INNER JOIN Participants p2 ON p1.matchID = p2.matchID
        INNER JOIN Matches m ON p1.matchID = m.matchID
        WHERE p1.summonerName = ? 
            AND p2.summonerName = ? 
            AND p1.teamID = p2.teamID
            AND p1.teamID = m.matchresult;
    ''', participant1, participant2)

    matches_6 = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.kda) as avg_kda
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        GROUP BY p.summonerName;
    ''', participant1, participant2)

    avg_kda = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.kda) as avg_kda
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        AND EXISTS (
            SELECT 1
            FROM Participants p1
            INNER JOIN Participants p2 ON p1.matchID = p2.matchID
            INNER JOIN Matches m ON p1.matchID = m.matchID
            WHERE p1.summonerName = ?
            AND p2.summonerName = ?
            AND p1.teamID = p2.teamID
            AND p1.matchID = p.matchID
        )
        GROUP BY p.summonerName;
    ''', participant1, participant2, participant1, participant2)

    avg_kda_p0 = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.killParticipation) as avg_kill_participation
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        GROUP BY p.summonerName;
    ''', participant1, participant2)

    avg_kill_participation = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.killParticipation) as avg_kill_participation
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        AND EXISTS (
            SELECT 1
            FROM Participants p1
            INNER JOIN Participants p2 ON p1.matchID = p2.matchID
            INNER JOIN Matches m ON p1.matchID = m.matchID
            WHERE p1.summonerName = ?
            AND p2.summonerName = ?
            AND p1.teamID = p2.teamID
            AND p1.matchID = p.matchID
        )
        GROUP BY p.summonerName;
    ''', participant1, participant2, participant1, participant2)

    avg_kill_participation_p0 = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.totalDamageDealtToChampions) as avg_total_damage_dealt_to_champions
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        GROUP BY p.summonerName;
    ''', participant1, participant2)

    avg_total_damage_dealt_to_champions = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.totalDamageDealtToChampions) as avg_total_damage_dealt_to_champions
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        AND EXISTS (
            SELECT 1
            FROM Participants p1
            INNER JOIN Participants p2 ON p1.matchID = p2.matchID
            INNER JOIN Matches m ON p1.matchID = m.matchID
            WHERE p1.summonerName = ?
            AND p2.summonerName = ?
            AND p1.teamID = p2.teamID
            AND p1.matchID = p.matchID
        )
        GROUP BY p.summonerName;
    ''', participant1, participant2, participant1, participant2)

    avg_total_damage_dealt_to_champions_p0 = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.physicalDamageDealtToChampions) as avg_physical_damage_dealt,
            AVG(p.magicDamageDealtToChampions) as avg_magic_damage_dealt,
            AVG(p.trueDamageDealtToChampions) as avg_true_damage_dealt
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        GROUP BY p.summonerName;
    ''', participant1, participant2)

    avg_damage_dealt_to_champions = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.physicalDamageDealtToChampions) as avg_physical_damage,
            AVG(p.magicDamageDealtToChampions) as avg_magic_damage,
            AVG(p.trueDamageDealtToChampions) as avg_true_damage
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        AND EXISTS (
            SELECT 1
            FROM Participants p1
            INNER JOIN Participants p2 ON p1.matchID = p2.matchID
            INNER JOIN Matches m ON p1.matchID = m.matchID
            WHERE p1.summonerName = ?
            AND p2.summonerName = ?
            AND p1.teamID = p2.teamID
            AND p1.matchID = p.matchID
        )
        GROUP BY p.summonerName;
    ''', participant1, participant2, participant1, participant2)

    avg_damage_dealt_to_champions_p0 = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.totalDamageDealtToChampions * 60.0 / m.matchDuration) as avg_damage_per_minute
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        GROUP BY p.summonerName;
    ''', participant1, participant2)

    avg_damage_dealt_per_minute = cursor.fetchall()

    cursor.execute('''
        SELECT 
            p.summonerName,
            AVG(p.totalDamageDealtToChampions / (m.matchDuration / 60.0)) as avg_damage_dealt_per_minute
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName IN (?, ?)
        AND EXISTS (
            SELECT 1
            FROM Participants p1
            INNER JOIN Participants p2 ON p1.matchID = p2.matchID
            INNER JOIN Matches m ON p1.matchID = m.matchID
            WHERE p1.summonerName = ?
            AND p2.summonerName = ?
            AND p1.teamID = p2.teamID
            AND p1.matchID = p.matchID
        )
        GROUP BY p.summonerName;
    ''', participant1, participant2, participant1, participant2)

    avg_damage_dealt_per_minute_p0 = cursor.fetchall()



    if isinstance(currentQueue, int):
        queue = "queue"
    else:
        queue = "queues"

    # Output the results

    print(f'Number of matches {participants[0]} played in the selected {queue}: {len(matches_1)}')
    print(f'Number of matches {participants[0]} played with {participants[1]} in the selected {queue}: {len(matches_3)}')
    print(f'Number of matches {participants[0]} played on the same team with {participants[1]} in the selected {queue}: {len(matches_5)}')
    print(f'Number of matches {participants[0]} played on the same team with {participants[1]} and won in the selected {queue}: {len(matches_6)}')
    print()

    try: 
        print(f'When playing togeather in the selected {queue} {participants[0]} and {participants[1]} have a {len(matches_6)/len(matches_5):.2f}% winrate togeather')
    except Exception as e:
            print(f'Error in calculating winrate: {e}')
            
    try:
        avg_kda_p1, avg_kda_p2 = [item[1] for item in avg_kda if item[0] == participant1][0], [item[1] for item in avg_kda if item[0] == participant2][0]
        print(f'When playing in the selected {queue} {participant1} and {participant2} have an average KDA of {avg_kda_p1:.2f} and {avg_kda_p2:.2f} respectively')
    except Exception as e:
        print(f'Error in calculating average KDA: {e}')

    try:
        avg_kda_p1, avg_kda_p2 = [item[1] for item in avg_kda_p0 if item[0] == participant1][0], [item[1] for item in avg_kda_p0 if item[0] == participant2][0]
        print(f'When playing in the selected {queue} {participant1} and {participant2} have an average KDA of {avg_kda_p1:.2f} and {avg_kda_p2:.2f} respectively')
    except Exception as e:
        print(f'Error in calculating average KDA (p0): {e}')

    try:
        avg_kill_participation_p1, avg_kill_participation_p2 = [item[1] for item in avg_kill_participation if item[0] == participant1][0], [item[1] for item in avg_kill_participation if item[0] == participant2][0]
        print(f'When playing in the selected {queue} {participant1} and {participant2} have an average team kill participation of {avg_kill_participation_p1:.2f} and {avg_kill_participation_p2:.2f} respectively')
    except Exception as e:
        print(f'Error in calculating average team kill participation: {e}')

    try:
        avg_kill_participation_p1, avg_kill_participation_p2 = [item[1] for item in avg_kill_participation_p0 if item[0] == participant1][0], [item[1] for item in avg_kill_participation_p0 if item[0] == participant2][0]
        print(f'When playing together in the selected {queue} {participant1} and {participant2} have an average team kill participation of {avg_kill_participation_p1:.2f} and {avg_kill_participation_p2:.2f} respectively')
    except Exception as e:
        print(f'Error in calculating average team kill participation (p0): {e}')

    try:
        avg_total_damage_dealt_to_champions_p1, avg_total_damage_dealt_to_champions_p2 = [item[1] for item in avg_total_damage_dealt_to_champions if item[0] == participant1][0], [item[1] for item in avg_total_damage_dealt_to_champions if item[0] == participant2][0]
        print(f'When playing in the selected {queue} {participant1} and {participant2} deal an average of {avg_total_damage_dealt_to_champions_p1} damage and {avg_total_damage_dealt_to_champions_p2} damage respectively')
    except Exception as e:
        print(f'Error in calculating average damage dealt: {e}')

    try:
        avg_total_damage_dealt_to_champions_p1, avg_total_damage_dealt_to_champions_p2 = [item[1] for item in avg_total_damage_dealt_to_champions_p0 if item[0] == participant1][0], [item[1] for item in avg_total_damage_dealt_to_champions_p0 if item[0] == participant2][0]
        print(f'When playing togeather in the selected {queue} {participant1} and {participant2} deal an average of {avg_total_damage_dealt_to_champions_p1} damage and {avg_total_damage_dealt_to_champions_p2} damage respectively')
    except Exception as e:
        print(f'Error in calculating average damage dealt (p0): {e}')

    try:
        avg_physical_damage_dealt_to_champions_p1, avg_physical_damage_dealt_to_champions_p2 = [item[1] for item in avg_damage_dealt_to_champions if item[0] == participant1][0], [item[1] for item in avg_damage_dealt_to_champions if item[0] == participant2][0]
        avg_magic_damage_dealt_to_champions_p1, avg_magic_damage_dealt_to_champions_p2 = [item[2] for item in avg_damage_dealt_to_champions if item[0] == participant1][0], [item[2] for item in avg_damage_dealt_to_champions if item[0] == participant2][0]
        avg_true_damage_dealt_to_champions_p1, avg_true_damage_dealt_to_champions_p2 = [item[3] for item in avg_damage_dealt_to_champions if item[0] == participant1][0], [item[3] for item in avg_damage_dealt_to_champions if item[0] == participant2][0]
        print(f'When playing togeather in the selected {queue} {participant1} and {participant2} deal an average of {avg_physical_damage_dealt_to_champions_p1} physical damage, {avg_magic_damage_dealt_to_champions_p1} magic damage, {avg_true_damage_dealt_to_champions_p1} true damage and {avg_physical_damage_dealt_to_champions_p2} physical damage, {avg_magic_damage_dealt_to_champions_p2} magic damage, {avg_true_damage_dealt_to_champions_p2} true damage respectively')
    except Exception as e:
        print(f'Error in calculating average damage dealt: {e}')

    try:
        avg_physical_damage_dealt_to_champions_p1, avg_physical_damage_dealt_to_champions_p2 = [item[1] for item in avg_damage_dealt_to_champions_p0 if item[0] == participant1][0], [item[1] for item in avg_damage_dealt_to_champions_p0 if item[0] == participant2][0]
        avg_magic_damage_dealt_to_champions_p1, avg_magic_damage_dealt_to_champions_p2 = [item[2] for item in avg_damage_dealt_to_champions_p0 if item[0] == participant1][0], [item[2] for item in avg_damage_dealt_to_champions_p0 if item[0] == participant2][0]
        avg_true_damage_dealt_to_champions_p1, avg_true_damage_dealt_to_champions_p2 = [item[3] for item in avg_damage_dealt_to_champions_p0 if item[0] == participant1][0], [item[3] for item in avg_damage_dealt_to_champions_p0 if item[0] == participant2][0]
        print(f'When playing togeather in the selected {queue} {participant1} and {participant2} deal an average of {avg_physical_damage_dealt_to_champions_p1} physical damage, {avg_magic_damage_dealt_to_champions_p1} magic damage, {avg_true_damage_dealt_to_champions_p1} true damage and {avg_physical_damage_dealt_to_champions_p2} physical damage, {avg_magic_damage_dealt_to_champions_p2} magic damage, {avg_true_damage_dealt_to_champions_p2} true damage respectively')
    except Exception as e:
        print(f'Error in calculating average damage dealt (p0): {e}')

    try:
        avg_damage_dealt_per_minute_p1, avg_damage_dealt_per_minute_p2 = [item[1] for item in avg_damage_dealt_per_minute if item[0] == participant1][0], [item[1] for item in avg_damage_dealt_per_minute if item[0] == participant2][0]
        print(f'When playing in the selected {queue} {participant1} and {participant2} deal an average of {avg_damage_dealt_per_minute_p1:.2f} damage per minute and {avg_damage_dealt_per_minute_p2:.2f} damage per minute respectively')
    except Exception as e:
        print(f'Error in calculating average damage per minute: {e}')

    try:
        avg_damage_dealt_per_minute_p1, avg_damage_dealt_per_minute_p2 = [item[1] for item in avg_damage_dealt_per_minute_p0 if item[0] == participant1][0], [item[1] for item in avg_damage_dealt_per_minute_p0 if item[0] == participant2][0]
        print(f'When playing togeather in the selected {queue} {participant1} and {participant2} deal an average of {avg_damage_dealt_per_minute_p1:.2f} damage per minute and {avg_damage_dealt_per_minute_p2:.2f} damage per minute respectively')
    except Exception as e:
        print(f'Error in calculating average damage per minute (p0): {e}')



#function calls in order to skip different functions of the program is the accompanying flag is False
#if apiFlag:
   # api_calls()

#if previewFlag:
    #preview_database()

#if queryFlag:
    #query_database()


# Close the cursor and the database connection
#cursor.close()
#conn.close()