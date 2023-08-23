const apiKey = 'RGAPI-fabe95d5-c516-44f8-a10d-04732015e2aa'; // Replace with your own API key
const region = 'na1'; // Replace with your own region
const summonerName = '7u87p1Czhiuq'; // Replace with your own summoner name

const url = `https://${region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/${summonerName}?api_key=${apiKey}`;

fetch(url)
  .then(response => response.json())
  .then(data => {
    const accountId = data.accountId;
    console.log(`Your account ID is ${accountId}`);
  })
  .catch(error => {
    console.error(error);
  });
