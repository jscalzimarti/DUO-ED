import requests

counter = 0
counter2 = 0
match_info = []

def fetch_match_data(matchId, apiKey):
    url3 = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={apiKey}'
    try:
        response3 = requests.get(url3)
        data3 = response3.json()
        
        match_info.append(matchId)
        
        teams = data3['info']['teams']
        for team in teams:
            if team['teamId'] == 100 and team['win']:
                match_info.append('BLUE')
            elif team['teamId'] == 200 and team['win']:
                match_info.append('RED')
        
        match_info.append(data3['info']['queueId'])

        match_info.append(data3['info']['gameDuration'])          #only works post patch 11.20
                                                            #new code will need to be implemented for querying anything previous to season 12

        participants = data3['info']['participants']
        
        for participant in participants:
            participant_data = [
                participant['summonerName'],
                participant['teamId'],
                'SUPPORT' if participant['teamPosition'] == 'UTILITY' else participant['teamPosition'],
                participant['championName'],
                round(participant['challenges']['kda'], 2),
                participant['kills'],
                participant['deaths'],
                participant['assists'],
                round(participant['challenges']['killParticipation'], 2),
                participant['physicalDamageDealtToChampions'],
                participant['magicDamageDealtToChampions'],
                participant['trueDamageDealtToChampions'],
                participant['totalDamageDealtToChampions']
            ]
            match_info.append(participant_data)



        global counter2
        counter2 += 1
        print(counter2)
        print(match_info)

        return match_info

    except Exception as e:
        print(e)