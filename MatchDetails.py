import requests

apiKey = 'RGAPI-da221bc0-65ee-4894-9b93-3b7653c963db'
region = 'na1'
summonerName = 'AYD Instinct'

url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={apiKey}'
response = requests.get(url)
data = response.json()
puuid = data['puuid']

url2 = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={apiKey}'
response2 = requests.get(url2)
matchIds = response2.json()

counter = 0

for matchId in matchIds:
    if counter < 1:
        url3 = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={apiKey}'
        response3 = requests.get(url3)
        data3 = response3.json()
        participants = data3['metadata']['participants']
        teams = data3['info']['teams']
        print(data3)
        print(teams)
    counter += 1
