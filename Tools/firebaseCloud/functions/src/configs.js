var rp = require('request-promise');
const common = require('./common');

async function getTournamentConfigFromParse(tournamentName, parseAppName) {
  
  let requiredConfigID = tournamentName.toUpperCase();
  var parseURL = common.Parse_URL.replace('PARSE_APP_NAME',parseAppName)+ "Tournaments.json";
  console.log(`umair::TournamentConfgi::URL::${parseURL}`);
  try {
    var options = {
      uri: parseURL,
      method: 'GET',
      gzip: true,
      resolveWithFullResponse: true,
      headers: {
        'Accept-Encoding': 'gzip',
        'cache-control': 'no-cache',
        'pragma': 'no-cache'
      }
    };
    let validConfig = null;
    var resp = await rp(options);
    // fs.writeFileSync('parseconfig.json', resp.body)
    const jsonObject = JSON.parse(resp.body)
    for (var element of jsonObject.results) 
    {
        if (element.TournamentID.toUpperCase() === requiredConfigID) 
        {
          let objectID = element.objectId;
          let startDayTimeStamp = element.StartTimeStamp === undefined ?  0 : element.StartTimeStamp;
          let endDayTimeStamp = element.EndTimeStamp === undefined ?  9007199254740991 : element.EndTimeStamp;
          console.log(`umair::ConfigTime::${startDayTimeStamp}}::${endDayTimeStamp}`);

          let currentTime = Number(Date.now()/1000);
          let isEndTimeValid =  (currentTime < endDayTimeStamp) ;
          let isStartTimeEarlierThanLastConfig =  validConfig != null ? (startDayTimeStamp < validConfig.StartTimeStamp) : true;
          if (isEndTimeValid && isStartTimeEarlierThanLastConfig)
          {
            
            console.log(`umair::ConfigFound::${element.TournamentID}}::${objectID}`);
            validConfig = element;
          }
        }
    }
    return validConfig;
  } catch (error) {
    console.error('Unable to get template');
    return null;
  }
}


async function getExplorerMissionsConfigFromParse(explorerMissionID, parseAppName) {
  
  var parseURL = common.Parse_URL.replace('PARSE_APP_NAME',parseAppName)+ "ExplorerMissions.json";
  let requiredConfigID = explorerMissionID.toUpperCase();
  try {
    var options = {
      uri: parseURL,
      method: 'GET',
      gzip: true,
      resolveWithFullResponse: true,
      headers: {
        'Accept-Encoding': 'gzip',
        'cache-control': 'no-cache',
        'pragma': 'no-cache'
      }
    };
    let validConfig = null;
    var resp = await rp(options);
    // fs.writeFileSync('parseconfig.json', resp.body)
    const jsonObject = JSON.parse(resp.body)
    for (var element of jsonObject.results) 
    {
      let configID = element.explorerMissionID.toUpperCase();
      if (configID == requiredConfigID) 
      {
        let objectID = element.objectId;
        let startDayTimeStamp = element.startDayTimeStamp === undefined ?  0 : element.startDayTimeStamp;
        let endDayTimeStamp = element.endDayTimeStamp === undefined ?  0 : element.endDayTimeStamp;;  
        let currentTime = Number(Date.now()/1000);
        let isEndTimeValid =  endDayTimeStamp != 0 ? (currentTime < endDayTimeStamp) : true;
        let isStartTimeEarlierThanLastConfig =  validConfig != null ? (startDayTimeStamp < validConfig.startDayTimeStamp) : true;
        if (isEndTimeValid && isStartTimeEarlierThanLastConfig)
        {
          
          console.log(`umair::ConfigFound::${configID}}::${objectID}`);
          validConfig = element;
        }
      }
    }
    return validConfig;
  } catch (error) {
    console.log(`Unable to get template`);
    console.error('Unable to get template');
    return null;
  }
}


module.exports = {
  getTournamentConfigFromParse,
  getExplorerMissionsConfigFromParse,
}
