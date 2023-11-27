import pyodbc

def duoStats(participant1, participant2):
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=DUOED;'
                      'Trusted_Connection=yes;')

    cursor = conn.cursor()

    # sql query to find the number of matches played on the same team
    cursor.execute('''
        select p1.matchID, p1.summonerName as participant1, p2.summonerName as participant2
        from Participants p1
        inner join Participants p2 on p1.matchID = p2.matchID
        where p1.summonerName = ? and p2.summonerName = ? and p1.teamID = p2.teamID;
    ''', participant1, participant2)

    matches_5 = cursor.fetchall()
    matches = len(matches_5)

    if matches:
        matches = matches
    else:
        matches = 0  # or any default value

    # query for duo page
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
    try:
        winrate = round(len(matches_6)/matches, 2)
    except:
        winrate = 0
        print(e)

    if winrate:
        winrate = winrate
    else:
        winrate = 0 

    cursor.execute('''
        SELECT 
        AVG(p.kda) as avg_kda
    FROM Participants p
    INNER JOIN Matches m ON p.matchID = m.matchID
    WHERE p.summonerName = ?
    ''', participant1)

    avg_kda_p1 = cursor.fetchall()

    cursor.execute('''
        SELECT 
        AVG(p.kda) as avg_kda
    FROM Participants p
    INNER JOIN Matches m ON p.matchID = m.matchID
    WHERE p.summonerName = ?
    ''', participant2)

    avg_kda_p2 = cursor.fetchall()

    avg_kda = (avg_kda_p2[0][0]+avg_kda_p1[0][0])/2

    if avg_kda:
        avg_kda = avg_kda
    else:
        avg_kda = 0 
    
    cursor.execute('''
        SELECT 
        AVG(p.killParticipation) as kill_participation
    FROM Participants p
    INNER JOIN Matches m ON p.matchID = m.matchID
    WHERE p.summonerName = ?
    ''', participant1)

    kill_participation_p1 = cursor.fetchall()

    cursor.execute('''
        SELECT 
        AVG(p.killParticipation) as kill_participation
    FROM Participants p
    INNER JOIN Matches m ON p.matchID = m.matchID
    WHERE p.summonerName = ?
    ''', participant2)

    kill_participation_p2 = cursor.fetchall()

    kill_participation = (kill_participation_p1[0][0]+kill_participation_p2[0][0])/2

    if kill_participation:
        kill_participation = kill_participation
    else:
        kill_participation = 0

    cursor.execute('''
        SELECT 
            AVG(p.totalDamageDealtToChampions) as avg_total_damage_dealt_to_champions
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName = ?
    ''', participant1)

    avg_damage_dealt_to_champions_p1 = cursor.fetchall()

    cursor.execute('''
        SELECT 
            AVG(p.totalDamageDealtToChampions) as avg_total_damage_dealt_to_champions
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName = ?
    ''', participant2)

    avg_damage_dealt_to_champions_p2 = cursor.fetchall()

    avg_damage_dealt_to_champions = (avg_damage_dealt_to_champions_p1[0][0]+avg_damage_dealt_to_champions_p2[0][0])/2

    if avg_damage_dealt_to_champions:
        avg_damage_dealt_to_champions = avg_damage_dealt_to_champions
    else:
        avg_damage_dealt_to_champions = 0
    
    cursor.execute('''
        SELECT 
            AVG(p.totalDamageDealtToChampions * 60.0 / m.matchDuration) as avg_damage_dealt_per_minute 
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName = ?
    ''', participant1)

    avg_damage_dealt_per_minute_p1 = cursor.fetchall()

    cursor.execute('''
        SELECT 
            AVG(p.totalDamageDealtToChampions * 60.0 / m.matchDuration) as avg_damage_dealt_per_minute 
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName = ?
    ''', participant2)

    avg_damage_dealt_per_minute_p2 = cursor.fetchall()

    avg_damage_dealt_per_minute = (avg_damage_dealt_per_minute_p1[0][0]+avg_damage_dealt_per_minute_p2[0][0])/2

    if avg_damage_dealt_per_minute:
        avg_damage_dealt_per_minute = round(avg_damage_dealt_per_minute)
    else:
        avg_damage_dealt_per_minute = 0

    return matches, winrate, avg_kda, kill_participation, avg_damage_dealt_to_champions, avg_damage_dealt_per_minute