import requests
import pyodbc

apiKey = 'RGAPI-6b11f5d7-14d3-4a9b-a144-3616be07bc22'
region = 'na1'
summonerName = 'AYD Instinct'
start = 0
count = 20

url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={apiKey}'
response = requests.get(url)
data = response.json()
puuid = data['puuid']

url2 = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&api_key={apiKey}'
response2 = requests.get(url2)
matchIds = response2.json()

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
            if team['teamId'] == '100' and team['win']:
                print("Team RED has won this match.")
                break
            else:
                print("Team BLUE has won this match.")
                break

        participants = data3['info']['participants']
        
        for participant in participants:
            summoner_name = participant['summonerName']
            win = participant['win']
            matchInfo.append(summoner_name)
            if win:
                matchInfo.append("win")
            else:
                matchInfo.append("loss")
        global counter2
        counter2 += 1
        print(counter2)
    except Exception as e:
        print(e)

for matchId in matchIds[:20]:
    if counter < 1:
        fetch_match_data(matchId)
    counter += 1

print (matchInfo)





'''
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=DUOED;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

insert_query = "INSERT INTO DBO.Matches (matchID, matchResult) VALUES (?, ?)"

# Execute the query with the values
cursor.execute(insert_query, (matchInfo[1], matchInfo[2]))

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
'''