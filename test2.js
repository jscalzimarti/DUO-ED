const apiKey = 'RGAPI-e1ce4bc1-1d8e-4bc6-8add-168fd0b78990';
const region = 'na1';
const summonerName = 'AYD Instinct';
const id = '-qQRHsniBjRz7dKNXAuh1iQPzjEtPnz9V24RtQFkl9B-JN4';
const accountId = 'l4d3EqES5SVLdQsjH5X_4VcHv0C89l63h-zZPGKz__8CajE'
const puuid = 'Urr54yOi2hANExfm1uS6W7OUnBxWSAUFiaoIsnkJlY3goRnFUbjccAS_S19YVwR6awIvlytVm0HgTA';

//const url = `https://${region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/${summonerName}?api_key=${apiKey}`;
//const url = `https://${region}.api.riotgames.com/lol/match/v5/matches/by-puuid/${puuid}?api_key=${apiKey}`;
const url = `https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/Urr54yOi2hANExfm1uS6W7OUnBxWSAUFiaoIsnkJlY3goRnFUbjccAS_S19YVwR6awIvlytVm0HgTA/ids?start=0&count=20&api_key=RGAPI-fabe95d5-c516-44f8-a10d-04732015e2aa`
//const url = `https://americas.api.riotgames.com/lol/match/v5/matches/NA1_4647776201?api_key=RGAPI-fabe95d5-c516-44f8-a10d-04732015e2aa`;
//const url = `https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/Urr54yOi2hANExfm1uS6W7OUnBxWSAUFiaoIsnkJlY3goRnFUbjccAS_S19YVwR6awIvlytVm0HgTA?api_key=RGAPI-fabe95d5-c516-44f8-a10d-04732015e2aa`;
fetch(url)

  .then(response => {
    console.log(response.headers.get('X-App-Rate-Limit'));
    console.log(response.headers.get('X-App-Rate-Limit-Count'));
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error(error));
