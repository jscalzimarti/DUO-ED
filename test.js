const apiKey = 'RGAPI-fabe95d5-c516-44f8-a10d-04732015e2aa'; // Replace with your own API key
const region = 'na1'; // Replace with your own region
const summonerName = 'AYD Valhaya'; // Replace with your own summoner name
const accountId = ''; // Replace with your own account ID

const url = `https://${region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/${summonerName}?api_key=${apiKey}`;

fetch(url)
  .then(response => response.json())
  .then(data => {
    const accountId = data.accountId;
    console.log(`Your account ID is ${accountId}`);
  })


const url2 = `https://${region}.api.riotgames.com/lol/match/v4/matchlists/by-account/${accountId}?api_key=${apiKey}`;

fetch(url2)
  .then(response => response.json())
  .then(data => {
    // Process the API response data here
    console.log(data);
  })
  .catch(error => {
    // Handle errors here
    console.error(error);
  });