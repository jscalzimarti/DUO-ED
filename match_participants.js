const apiKey = 'RGAPI-d25635a4-aee9-438e-9d91-554cb4721b59';
const region = 'na1';
//const summonerName = '7u87p1Czhiuq';
const summonerName = 'AYD Instinct';
const start = 0;
const count = 20;

const url = `https://${region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/${summonerName}?api_key=${apiKey}`;
//console.log(url);
fetch(url)
  .then(response => response.json())
  .then(data => {
    const puuid = data.puuid;
    //console.log(puuid);

    const url2 = `https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/${puuid}/ids?start=${start}&count=${count}&api_key=${apiKey}`;
    return fetch(url2);
  })
  .then(response => response.json())
  .then(data => {
    const matchIds = data;
    //console.log(matchIds);

    let counter = 0;
    let counter2 = 0;
    async function fetchMatchData(matchId) {
        const url3 = `https://americas.api.riotgames.com/lol/match/v5/matches/${matchId}?api_key=${apiKey}`;
        try {
          const response = await fetch(url3);
          const data = await response.json();
          const participants = data.info.participants;
          participants.forEach((participant) => {
            const summonerName = participant.summonerName;
            const win = participant.win;
            console.log(summonerName);
            if (win) {
              console.log("win");
            } else {
              console.log("loss");
            }
          });
          console.log(matchId);
          counter2++;
          console.log(counter2);
          console.log("\n");
        } catch (error) {
          console.error(error);
        }
      }
      
      (async () => {
        for (const matchId of matchIds.slice(0, 20)) {
          if (counter < 20) {
            //console.log(matchId);
            await fetchMatchData(matchId);
          }
          counter++;
        }
      })();
            
  })
  .catch(error => console.error(error))


