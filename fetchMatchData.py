import requests

counter = 0
counter2 = 0
matchInfo = []

def fetch_match_data(matchId, apiKey):
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

        return matchInfo

    except Exception as e:
        print(e)