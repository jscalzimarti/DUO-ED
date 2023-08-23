import requests

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

def fetch_match_data(matchId):
    url3 = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={apiKey}'
    try:
        response3 = requests.get(url3)
        data3 = response3.json()
        participants = data3['info']['participants']
        for participant in participants:
            summoner_name = participant['summonerName']
            win = participant['win']
            print(summoner_name)
            if win:
                print("win")
            else:
                print("loss")
        print(matchId)
        global counter2
        counter2 += 1
        print(counter2)
        print()
    except Exception as e:
        print(e)

for matchId in matchIds[:20]:
    if counter < 20:
        fetch_match_data(matchId)
    counter += 1
