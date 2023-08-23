const apiKey = 'RGAPI-e1ce4bc1-1d8e-4bc6-8add-168fd0b78990';
const region = 'na1';
//const summonerName = '7u87p1Czhiuq';
const summonerName = 'AYD Instinct';

const url = `https://${region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/${summonerName}?api_key=${apiKey}`;
//console.log(url);
fetch(url)
  .then(response => response.json())
  .then(data => {
    const puuid = data.puuid;
    //console.log(puuid);

    const url2 = `https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/${puuid}/ids?start=0&count=20&api_key=${apiKey}`;
    return fetch(url2);
  })
  .then(response => response.json())
  .then(data => {
    const matchIds = data;
    //console.log(matchIds);

    let counter = 0;
    matchIds.forEach(matchId => {
      if (counter < 1) {
        const url3 = `https://americas.api.riotgames.com/lol/match/v5/matches/${matchId}?api_key=${apiKey}`;
        fetch(url3)
        .then(response => response.json())   
        .then(data => {
          const participants = data.metadata.participants;
          const teams = data.info.teams;
          console.log(data);
          console.log(teams);

        })
      }
      counter++;
    })
  })
  .catch(error => console.error(error))


