import requests

def find_match_timestamp(matchId, apiKey):    
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={apiKey}'
    try:
        response = requests.get(url)
        data = response.json()
        timestamp = data['info']['gameCreation']
        return timestamp
    except Exception as e:
        print(e)