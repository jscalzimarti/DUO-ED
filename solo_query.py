import pyodbc

def soloStats(league_account):

    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=DUOED;'
                      'Trusted_Connection=yes;')

    cursor = conn.cursor()

    # SQL query to find number of matches league_account played
    cursor.execute("SELECT COUNT(*) FROM dbo.Participants where summonerName = ?", league_account)

    # Fetch the results
    matches = cursor.fetchall()

    if matches:
        matches = matches[0][0]
    else:
        matches = 0  # or any default value

    cursor.execute('''
        SELECT 
            (COUNT(CASE WHEN p1.teamID = m.matchResult THEN 1 END) * 100.0) / NULLIF(COUNT(*), 0) as winrate_percentage
        FROM Participants p1
        INNER JOIN Matches m ON p1.matchID = m.matchID
        WHERE p1.summonerName = ?
    ''', league_account)

    winrate_solo = cursor.fetchall()

    if winrate_solo:
        winrate_solo = winrate_solo[0][0]
    else:
        winrate_solo = 0 

    #SQL query to find the average KDA of both players
    cursor.execute('''
        SELECT 
        AVG(p.kda) as avg_kda
    FROM Participants p
    INNER JOIN Matches m ON p.matchID = m.matchID
    WHERE p.summonerName = ?
    ''', league_account)

    avg_kda = cursor.fetchall()

    if avg_kda:
        avg_kda = avg_kda[0][0]
    else:
        avg_kda = 0 

    #SQL query to find the average KDA of both players
    cursor.execute('''
        SELECT 
        AVG(p.killParticipation) as kill_participation
    FROM Participants p
    INNER JOIN Matches m ON p.matchID = m.matchID
    WHERE p.summonerName = ?
    ''', league_account)

    kill_participation = cursor.fetchall()

    if kill_participation:
        kill_participation = kill_participation[0][0]
    else:
        kill_participation = 0
    
    #SQL query to find the average KDA of both players
    cursor.execute('''
        SELECT 
            AVG(p.totalDamageDealtToChampions) as avg_total_damage_dealt_to_champions
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName = ?
    ''', league_account)

    avg_damage_dealt_to_champions = cursor.fetchall()

    if avg_damage_dealt_to_champions:
        avg_damage_dealt_to_champions = avg_damage_dealt_to_champions[0][0]
    else:
        avg_damage_dealt_to_champions = 0

    cursor.execute('''
        SELECT 
            AVG(p.totalDamageDealtToChampions * 60.0 / m.matchDuration) as avg_damage_dealt_per_minute 
        FROM Participants p
        INNER JOIN Matches m ON p.matchID = m.matchID
        WHERE p.summonerName = ?
    ''', league_account)

    avg_damage_dealt_per_minute = cursor.fetchall()

    if avg_damage_dealt_per_minute:
        avg_damage_dealt_per_minute = avg_damage_dealt_per_minute[0][0]
    else:
        avg_damage_dealt_per_minute = 0

    return matches, winrate_solo, avg_kda, kill_participation, avg_damage_dealt_to_champions, avg_damage_dealt_per_minute