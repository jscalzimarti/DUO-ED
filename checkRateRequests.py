import requests


def find_match_queue(matchId, apiKey):    
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={apiKey}'
    response = requests.get(url)
    x_app_rate_limit = response.headers.get('X-App-Rate-Limit')
    x_app_rate_limit_count = response.headers.get('X-App-Rate-Limit-Count')
    data = response.json()
    queueId = data['info']['queueId']
    print("X-App-Rate-Limit:", x_app_rate_limit)
    print("X-App-Rate-Limit-Count:", x_app_rate_limit_count)
    print(queueId)

find_match_queue('NA1_4748564367', 'RGAPI-da221bc0-65ee-4894-9b93-3b7653c963db')
