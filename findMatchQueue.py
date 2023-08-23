import requests

def find_match_queue(matchId, apiKey):    
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={apiKey}'
    response = requests.get(url)
    data = response.json()
    queueId = data['info']['queueId']
    return queueId

#print(find_match_queue('NA1_4748564367', 'RGAPI-da221bc0-65ee-4894-9b93-3b7653c963db'))