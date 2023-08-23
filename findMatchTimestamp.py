import requests

def find_match_timestamp(matchId, apiKey):    
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={apiKey}'
    response = requests.get(url)
    data = response.json()
    timestamp = data['info']['gameCreation']
    return timestamp

#print(find_match_timestamp('NA1_4748564367', 'RGAPI-da221bc0-65ee-4894-9b93-3b7653c963db'))