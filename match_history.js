const apiKey = 'RGAPI-fabe95d5-c516-44f8-a10d-04732015e2aa';
const region = 'na1';
const summonerName = 'AYD Instinct';

const id = '-qQRHsniBjRz7dKNXAuh1iQPzjEtPnz9V24RtQFkl9B-JN4';
const accountId = 'l4d3EqES5SVLdQsjH5X_4VcHv0C89l63h-zZPGKz__8CajE'
const puuid2 = 'Urr54yOi2hANExfm1uS6W7OUnBxWSAUFiaoIsnkJlY3goRnFUbjccAS_S19YVwR6awIvlytVm0HgTA';

const url = `https://${region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/${summonerName}?api_key=${apiKey}`;
fetch(url)
  .then(response => response.json())
  .then(data => {
    const puuid = data.puuid;
    console.log(puuid);

    const url2 = `https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/${puuid}/ids?start=0&count=20&api_key=${apiKey}`;
    return fetch(url2);
  })
  .then(response => response.json())
  .then(data => {
    const matchIds = data;
    console.log(matchIds);
    console.log(data);

    matchIds.forEach(matchId => {
      const url3 = `https://americas.api.riotgames.com/lol/match/v5/matches/${matchId}?api_key=${apiKey}`;
      fetch(url3)
      .then(response => {
        return response.json();  
       })   
       .then(data => console.log(data))
    })
  })
  .catch(error => console.error(error))

//const url = `https://${region}.api.riotgames.com/lol/match/v5/matches/by-puuid/${puuid2}?api_key=${apiKey}`;
//const url = `https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/Urr54yOi2hANExfm1uS6W7OUnBxWSAUFiaoIsnkJlY3goRnFUbjccAS_S19YVwR6awIvlytVm0HgTA/ids?start=0&count=20&api_key=RGAPI-fabe95d5-c516-44f8-a10d-04732015e2aa`
//const url = `https://americas.api.riotgames.com/lol/match/v5/matches/NA1_4647776201?api_key=RGAPI-fabe95d5-c516-44f8-a10d-04732015e2aa`;
const url4 = `https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/Urr54yOi2hANExfm1uS6W7OUnBxWSAUFiaoIsnkJlY3goRnFUbjccAS_S19YVwR6awIvlytVm0HgTA?api_key=RGAPI-fabe95d5-c516-44f8-a10d-04732015e2aa`;
fetch(url4)
  .then(response => {
    console.log(response.headers.get('X-App-Rate-Limit'));
    console.log(response.headers.get('X-App-Rate-Limit-Count'));
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error(error));
