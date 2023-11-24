#    Function to query the DUOED database for various statistics and information based on specified participants.
#
#    Args:
#    participants (list): A list containing summoner names of participants.
#
#    Returns:
#    None

import pyodbc

def query_database(participants):   #participants is a list passed by the website
                                    #IT CANNOT BE A SINGLE VALUE IN THIS CODE

                        #Queue should be an arguement passed by the website
    currentQueue = 420  #code can accept multiple queues as an arguement (syntax: 0, 420, 700) 

    participant1 = participants[0]
    participant2 = participants[1]
    participant3 = participants[2]
    participant4 = participants[3]
    participant5 = participants[4]

    participant6 = participants[5]
    participant7 = participants[6]
    participant8 = participants[7]
    participant9 = participants[8]
    participant10 = participants[9]

    # Establish a connection to the database
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=DUOED;'
                      'Trusted_Connection=yes;')

    # Create a cursor to interact with the database
    cursor = conn.cursor()
 
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

    #SQL query to find the average KDA of both players
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

    #SQL query to find the average KDA of both players when they are in the same game
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

    #SQL query to find the average kill participation of both players
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

    #SQL query to find the average kill participation of both players when they are in the same game
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

    #SQL query to find the average total damage dealt to champions of both players
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

    #SQL query to find the average total damage dealt to champions of both players when in the same game
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

    #SQL query to find the average damage dealt to champions(broken up into physical, magic and true damage) of both players
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

    #SQL query to find the average damage dealt to champions(broken up into physical, magic and true damage) of both players when in the same game
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

    #SQL query to find the average damage dealt to champions per minute of both players
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

    #SQL query to find the average damage dealt to champions per minute of both players while in the same game
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
    
    # Close the cursor and the database connection
    cursor.close()
    conn.close()