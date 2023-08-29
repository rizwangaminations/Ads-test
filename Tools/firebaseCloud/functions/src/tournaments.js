const common = require('./common');
const DDNA = require('./DDNA');

const configurations = require('./configs');
const { del } = require('request-promise');
const KEY_INBOX_REWARD = 'reward';
const KEY_INBOX_RANK = 'rank';
const KEY_INBOX_REWARD_TYPE = 'type';
const KEY_INBOX_REWARD_TIME = 'time';
const TOURNAMENT_OFFER = 'offerid';
const TOURNAMENT_MULTIPLIER = 'multiplier';

const KEY_DELAY = 'delay';
const KEY_DURATION = 'duration';
const KEY_RESULT_TIME = 'resultTime';
const KEY_TOURNAMENT_NAME = 'name';
const KEY_PARSE_APP = 'parse';
const KEY_RTP = 'rtp';
const KEY_START_PRIZE = 'startPrize';
const KEY_SPLIT_REST = 'split';
const KEY_BRACKET = 'bracket';
const KEY_TOP_RANKS = 'topRanks';
const KEY_STOP_TOURNAMENT = 'stop';
const KEY_TOURNAMENT_TYPE = 'type';
const KEY_EXPLORER_NAME = 'explorer';
const KEY_EXPLORER_LOOP_ID = 'loopID';
const KEY_EXPLORER_CONFIG_VERSION = 'configVersion';


const TournamentType = {"Default":1, "Explorer":5};

const SetupExplorerTournament = async (req, res) => {
  try {
    let httpMessage = ""
    let httpStatus  = 0;
    let explorerName = (req.query.explorer || req.body.explorer || "")
    let explorerNameLower = explorerName.toLowerCase()
    let parseAppName = (req.query.parse || req.body.parse || "")
    let isStartingNew = true;
    let tournamentName = "";
    let result = await SetupExplorerTournamentInternal(explorerNameLower, parseAppName, isStartingNew, tournamentName);
    httpMessage =  result.message; 
    httpStatus = result.status ? 200 : 500;
    console.log(httpMessage);
    res.status(httpStatus).send(httpMessage);
  } catch (e) {
    console.error(e);
    res.status(500).send(e);
  }
};

async function SetupExplorerTournamentInternal(explorerName, parseAppName, isStartingNew, oldTournamentName)
{
  let tournamentType = TournamentType.Explorer;
  let message = ""
  let status  = false;
  let configNotFound = false; 
  if (!isStartingNew || parseAppName === "")
  {
    parseAppName = common.PARSE_APP_NAME;
    console.log(`UMAIR::USING LATEST PARSE ${parseAppName}`);
  }
  let explorerConfigs = await configurations.getExplorerMissionsConfigFromParse(explorerName, parseAppName);
  if (explorerConfigs === null)
  {
    configNotFound = true;
    message = "ExplorerMissions::setupTournament::ExplorerMissionsConfigsNotFound::" + explorerName; 
    status  = false;  
  }
  else
  {
    let tournamentNameRaw = explorerConfigs.tournamentID;
    let tournamentName = tournamentNameRaw.toLowerCase()
    let tournamentConfigs = await GetTournamentCustomConfigs(tournamentName, parseAppName);
    if (tournamentConfigs === null)
    {
      configNotFound = true;
      message = "Tournaments::setupTournament::TournamentConfigsNotFound::" + tournamentName; 
      status  = false;  
    }
    else
    {
      let missionLoopDays = explorerConfigs.missionLoopDays;
      let tournamentDuration = missionLoopDays * 24*60*60;
      let startDayTimeStamp = explorerConfigs.startDayTimeStamp;
      let currentTimeStamp = Number(Date.now()/1000);
      let configVersion = explorerConfigs.configVersion;

      let tournamentStartDelay = 0;
      let loopID = 0;
      if (startDayTimeStamp > currentTimeStamp)
      {
        tournamentStartDelay =  startDayTimeStamp-currentTimeStamp;
        loopID = 1;
      }
      else
      {
        loopID =  Math.ceil((currentTimeStamp-startDayTimeStamp) / (tournamentDuration));
        let timeElapsed =  (currentTimeStamp-startDayTimeStamp) % (tournamentDuration);
        tournamentDuration =  (tournamentDuration - timeElapsed);
      }

      tournamentConfigs[KEY_TOURNAMENT_TYPE] =  tournamentType;
      tournamentConfigs[KEY_EXPLORER_NAME] = explorerName;
      tournamentConfigs[KEY_DELAY] =  tournamentStartDelay;
      tournamentConfigs[KEY_DURATION] =  tournamentDuration;
      tournamentConfigs[KEY_EXPLORER_LOOP_ID] =  loopID;
      tournamentConfigs[KEY_EXPLORER_CONFIG_VERSION] =  configVersion;

      let result = await ScheduleTournament(tournamentConfigs, isStartingNew);
      message =  result.message; 
      status = result.status;
    }
  }


  if (!status && !isStartingNew)
  {
    message = "Tournament::Stopping Tournament as Config does not exist::" + tournamentName; 
    let updates = {};
    let tournamentRootPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/`;
    updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_STATUS_NODE}`] = common.TournamentStatus.STOPED;
    await common.firebaseAdmin.database().ref().update(updates);
    status  = true;  
  }
  
  return {message, status};
}

const SetupDefaultTournament = async (req, res) => {
  try {
    let httpMessage = ""
    let httpStatus  = 0;
    let tournamentName = (req.query.tournament || req.body.tournament || "")
    let tournamentNameLower = tournamentName.toLowerCase()
    let parseAppName = (req.query.parse || req.body.parse || "")
    let customDelay = (req.query.delay || req.body.delay || -1)
    let isStartingNew = true;
    let result = await SetupDefaultTournamentInternal(tournamentNameLower, parseAppName, customDelay, isStartingNew);
    httpMessage =  result.message; 
    httpStatus = result.status ? 200 : 500;
    console.log(httpMessage);
    res.status(httpStatus).send(httpMessage);
  } catch (e) {
    console.error(e);
    res.status(500).send(e);
  }
};

async function SetupDefaultTournamentInternal(tournamentName, parseAppName, customDelay, isStartingNew)
{
  let tournamentType = TournamentType.Default;
  let message = ""
  let status  = false;
  if (!isStartingNew || parseAppName === "")
  {
    parseAppName = common.PARSE_APP_NAME;
    console.log(`UMAIR::USING LATEST PARSE ${parseAppName}`);
  }
  let tournamentConfigs = await GetTournamentCustomConfigs(tournamentName, parseAppName);
  if (tournamentConfigs === null)
  {
    message = "Tournaments::setupTournament::TournamentConfigsNotFound::" + tournamentName; 
    status  = false;  
  }
  else
  {
    
    tournamentConfigs[KEY_TOURNAMENT_TYPE] =  tournamentType;
    if (customDelay != -1)
    {
      tournamentConfigs[KEY_DELAY] =  customDelay;
    }
    let result = await ScheduleTournament(tournamentConfigs, isStartingNew);
    message =  result.message; 
    status = result.status;
  }

  if (!status && !isStartingNew)
  {
    message = "Tournament::Stopping Tournament as Config does not exist::" + tournamentName; 
    let updates = {};
    let tournamentRootPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/`;
    updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_STATUS_NODE}`] = common.TournamentStatus.STOPED;
    await common.firebaseAdmin.database().ref().update(updates);
    status  = true;  
  }
  return {message, status};
}


async function GetTournamentCustomConfigs(tournamentName, parseAppName)
{
  let tournamentConfigs = await configurations.getTournamentConfigFromParse(tournamentName, parseAppName);
  if (tournamentConfigs != null)
  {
    let delayTime = tournamentConfigs.TournamentDelaySecs;
    let durationTime = tournamentConfigs.TournamentDurationSecs;
    let resultTime = tournamentConfigs.TournamentResultsInTimeSecs;
    let rtpFactor = tournamentConfigs.PrizePoolRTPFactor;
    let startingPrize = tournamentConfigs.PrizePoolStartingPrize;
    let splitRest = tournamentConfigs.PrizeDistributionSplitRestPopulationPerc
    let bracket = tournamentConfigs.PrizeDistributionPlayerPerBracket
    let topRanks = tournamentConfigs.PrizeDistributionTop
    let stopTournament = tournamentConfigs.StopTournament

    let tournamentCustomConfig = {};
    tournamentCustomConfig[KEY_DELAY] = delayTime;
    tournamentCustomConfig[KEY_DURATION] = durationTime;
    tournamentCustomConfig[KEY_RESULT_TIME] = resultTime;
    tournamentCustomConfig[KEY_TOURNAMENT_NAME] = tournamentName;
    tournamentCustomConfig[KEY_PARSE_APP] = parseAppName;
    tournamentCustomConfig[KEY_RTP] = rtpFactor;
    tournamentCustomConfig[KEY_START_PRIZE] = startingPrize;
    tournamentCustomConfig[KEY_SPLIT_REST] = splitRest;
    tournamentCustomConfig[KEY_BRACKET] = bracket;
    tournamentCustomConfig[KEY_TOP_RANKS] = topRanks;
    tournamentCustomConfig[KEY_STOP_TOURNAMENT] = stopTournament;

    return tournamentCustomConfig;
  }
  return null;

}

async function ScheduleTournament(customConfig, isStartingNew) {
  let status = false;
  let message = ""
  let delay = customConfig[KEY_DELAY];
  let tournamentName = customConfig[KEY_TOURNAMENT_NAME];
  let stopTournament = customConfig[KEY_STOP_TOURNAMENT];
  let tournamentRootPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/`;

  let tournamentRootRef = common.firebaseAdmin.database().ref(`${common.TOURNAMENT_DB_PATH}/${tournamentName}`)
  let tournamentStatus = await (await tournamentRootRef.child(`${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_STATUS_NODE}`).once('value')).val()
  let isTournamentPreparingResults = (tournamentStatus == common.TournamentStatus.PREPARING_RESULTS);
  let canRestart = !isStartingNew && isTournamentPreparingResults;
  let canStartNew =  (tournamentStatus == null || tournamentStatus == common.TournamentStatus.STOPED);
  if (!canStartNew && !canRestart) {
    message = "Tournaments::setupTournament::TournamentAlreadyRunningWithName::" + tournamentName; 
    status = false;
  }
  else if (stopTournament){
    message = "Tournament::ScheduleTournament::TournamentStoppedInConfig::" + tournamentName; 
    let updates = {};
    updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_STATUS_NODE}`] = common.TournamentStatus.STOPED;
    await common.firebaseAdmin.database().ref().update(updates);
    status  = true;  
  }
  else{
    if (delay > 0)
    {
      let endTime = Math.round(Number(Date.now()/1000) + Number(delay));
      let updates = {};
      updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_END_TIME_NODE}`] = endTime;
      updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_STATUS_NODE}`] = common.TournamentStatus.WAITING;
      await common.firebaseAdmin.database().ref().update(updates);
      let callbackURL = `https://${common.LOCATION}-${common.PROJECT}.cloudfunctions.net/${common.FUNCTION_START_TOURNAMENT}`;
      status = false;
      let payload = {configs: customConfig};
      let retryCount = 5;
      while(!status && retryCount>0)
      {
        retryCount--;
        status = await Umair_ScheduleCloudTask(callbackURL, endTime, payload, tournamentName+ "_start");  
      }
      if (!status)
      {
        console.error(new Error('Failed to schedule task'));
      }
    }
    else
    {
      let result = await Umair_StartTournament(customConfig);
      status = result.status;
    }
    message = "Tournament::ScheduleTournament::Status::" + (status ? "Success" : "Fail"); 
  }
  return {status, message};
}   



const Cloud_StartTournament = async (req, res) => {
  try {
    let configs = req.body.configs;
    let tournamentName = configs[KEY_TOURNAMENT_NAME];
    let httpMessage = ""
    let httpStatus  = 0;
    let result = await Umair_StartTournament(configs);
    httpStatus =  result.status ? 200 : 500;
    httpMessage = result.message;
    console.log(httpMessage);  
    res.status(httpStatus).send(httpMessage);
  } catch (error) {
    console.log(error);
    res.status(500).send(error);
  }
};

async function Umair_StartTournament(configs) { 
  let tournamentName = configs[KEY_TOURNAMENT_NAME];
  let tournamentRootPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/`;
  let tournamentRootRef = common.firebaseAdmin.database().ref(tournamentRootPath)
  let tournamentSessionID = await tournamentRootRef.child(`${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_SESSION_NODE}`).once('value')
  let previousSessionID = (tournamentSessionID.val() || 0);  
  let nextSessionID = previousSessionID + 1;  
  let oldSessionLeaderboardPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/${common.TOURNAMENT_LEADERBOARD_PATH}/`;

  let runTime = configs[KEY_DURATION];
  let endTime = Math.round(Date.now()/1000 + Number(runTime));
  let updates = {};
  updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_END_TIME_NODE}`] = endTime;
  updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_STATUS_NODE}`] = common.TournamentStatus.RUNNING;
  updates[tournamentRootPath + common.COINS_WAGERED] = null;
  updates[oldSessionLeaderboardPath] = null;
  updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_SESSION_NODE}`] = nextSessionID;
  await common.firebaseAdmin.database().ref().update(updates);
  await DDNA.postTournamentStartEvent(tournamentName, nextSessionID)
  
  let callbackURL = `https://${common.LOCATION}-${common.PROJECT}.cloudfunctions.net/${common.FUNCTION_STOP_TOURNAMENT}`;
  let status = false;
  let message = "";
  let payload = {configs: configs}
  let retryCount = 5;
  while(!status && retryCount>0)
  {
    retryCount--;
    status = await Umair_ScheduleCloudTask(callbackURL, endTime, payload, tournamentName + "_stop");
  }
  if (!status)
  {
    message = "Tournaments::StartTournament::FailedToScheduleTask";
    console.error(new Error('Failed to schedule task'));
  }
  else
  {
    message = "Tournaments::StartTournament::Started";
  }
  return {status, message};
}


const Cloud_StopTournament = async (req, res) => {
  try {
    let httpMessage = ""
    let httpStatus  = 0;

    let configs = req.body.configs
    let tournamentName =  configs[KEY_TOURNAMENT_NAME];
    let tournamentRootPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/`;
    let delay = configs[KEY_RESULT_TIME];
    let endTime = Math.round(Date.now()/1000 + Number(delay));

    var updates = {};
    updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_END_TIME_NODE}`] = endTime;
    updates[tournamentRootPath + `${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_STATUS_NODE}`] = common.TournamentStatus.PREPARING_RESULTS;
    await common.firebaseAdmin.database().ref().update(updates);

    var callbackURL = `https://${common.LOCATION}-${common.PROJECT}.cloudfunctions.net/${common.FUNCTION_WAITING_RESULT}`;
    let status = false;
    let payload = {configs: configs}
    let retryCount = 5;
    while(!status && retryCount>0)
    {
      retryCount--;
      status = await Umair_ScheduleCloudTask(callbackURL, endTime, payload, tournamentName + "_result");
    }
    if (!status)
    {
      console.error(new Error('Failed to schedule task'));
    }
    httpMessage = "Tournament::Cloud_StopTournament::Status::" + (status ? "Success" : "Fail");
    httpStatus =  status ? 200 : 500;
    console.log(httpMessage);
    res.status(httpStatus).send(httpMessage);

  } catch (error) {
    console.error(error);
    res.status(500).send(error);
  }
};


const Cloud_CalculateResults = async (req, res) => {
  try {
    let httpMessage = ""
    let httpStatus  = 0;
    var configs = req.body.configs

    var tournamentName = configs[KEY_TOURNAMENT_NAME];
    var parseAppName = configs[KEY_PARSE_APP];
    var tournamentType = TournamentType.Default;
    if( configs[KEY_TOURNAMENT_TYPE] !== undefined)
    {
      tournamentType = configs[KEY_TOURNAMENT_TYPE];
    }

    var tournamentRootPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/`;
    var tournamentRootRef = common.firebaseAdmin.database().ref(tournamentRootPath)
    var tournamentSessionID = await tournamentRootRef.child(`${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_SESSION_NODE}`).once('value')
    var currentSessionID = (tournamentSessionID.val() || 0);  
    await GenerateResults(currentSessionID, configs);

    let isStartingNew = false;
    let result = {};    
    switch (tournamentType)
    {
      case TournamentType.Default:
      {
        result = await SetupDefaultTournamentInternal(tournamentName, parseAppName, -1, isStartingNew);
      }
      break;
      case TournamentType.Explorer:
      {
        var explorerName = configs[KEY_EXPLORER_NAME];
        result = await SetupExplorerTournamentInternal(explorerName, parseAppName, isStartingNew, tournamentName);
      }
      break;
      default:
      {
        result["status"] = false;
      }
    }

    httpMessage = result.message;
    httpStatus = result.status ? 200 : 500;
    console.log(httpMessage);
    res.status(httpStatus).send(httpMessage);
  } catch (e) {
    console.error(e);
    res.status(500).send(e);
  }
};

async function GenerateResults(currentSessionID, configs) {   

  let tournamentName = configs[KEY_TOURNAMENT_NAME];
  var tournamentType = configs[KEY_TOURNAMENT_TYPE];

  let tournamentRootRef = common.firebaseAdmin.database().ref(`${common.TOURNAMENT_DB_PATH}/${tournamentName}`)
  let coinsWageredRef = tournamentRootRef.child(common.COINS_WAGERED);
  let coinsWagered = (await coinsWageredRef.once('value')).val();

  let scoreNodePath = `${common.TOURNAMENT_LEADERBOARD_PATH}/${currentSessionID}/${common.TOURNAMENT_LEADERBOARD_SCORE_NODE}`;
  let topXRef = tournamentRootRef.child(scoreNodePath).orderByChild('score');
  let topX = (await topXRef.once('value'));
  let totalPlayers = topX.numChildren();
  let totalPrize = 0;
  let userIDList = "";
  let userPrizeList = "";

  if (totalPlayers > 0)
  {
    let logString = "**********************Rewards**********************" + '\n';
    let rtpFactor = configs[KEY_RTP];
    let startingPrize = configs[KEY_START_PRIZE];
    let splitRest = configs[KEY_SPLIT_REST];
    let bracket = configs[KEY_BRACKET];
    let topRanks = configs[KEY_TOP_RANKS];
    let topXUsers = Math.min(totalPlayers, Math.ceil(totalPlayers * splitRest/100) + topRanks.length);
    totalPrize = Math.max(startingPrize, Math.ceil(coinsWagered * (rtpFactor/100)))


    logString = logString + `Total Coins Wagered: ${coinsWagered}` + '\n';
    logString = logString + `Total Players: ${totalPlayers}` + '\n';
    logString = logString + `Distribute ${totalPrize} in top ${topXUsers} players` + '\n';


    let prizeDistributionResult = DistributePrize(totalPrize, topXUsers, bracket, topRanks);

    let prizes =  prizeDistributionResult.prizes;
    userPrizeList =  prizeDistributionResult.prizeDistribution;

    var topXSorted = []
    topX.forEach(playerSnapshot => {
      let childKey = playerSnapshot.key;
      topXSorted.push(childKey);
    });

    topXSorted.reverse();
    let count = 0;
    let updates = {};
    let i=0;
    for (i = 0 ; i<totalPlayers  ; i++)
    {
      // i<topXUsers
      let prizeValue =  (i<topXUsers) ? prizes[i] : 0;
      logString = logString + `Position::${i+1},      ${topXSorted[i]},       Reward::${prizeValue}` + '\n';
      let tournamentNameKey = `${tournamentName}_${currentSessionID}`;

      let inboxReward = {}
      inboxReward[KEY_INBOX_REWARD] = prizeValue;
      inboxReward[KEY_INBOX_RANK] = i+1;
      inboxReward[KEY_INBOX_REWARD_TYPE] = tournamentType;
      inboxReward[KEY_INBOX_REWARD_TIME] = common.firebaseAdmin.database.ServerValue.TIMESTAMP;      

      switch (tournamentType)
      {
        case TournamentType.Default:
        {
          if (prizeValue > 0)
          {
            var userOfferRef = common.firebaseAdmin.database().ref(`${common.USERS_DB_PATH}/${topXSorted[i]}/${TOURNAMENT_OFFER}`)
            let tournamentOffer = (await userOfferRef.once('value')).val();
            // console.log(`umair::PlayerID::${topXSorted[i]}::OfferID::${tournamentOffer}::Multiplier::${offerMultiplier}`);
    
            if (tournamentOffer !== null)
            {
              var userOfferMultiplierRef = common.firebaseAdmin.database().ref(`${common.USERS_DB_PATH}/${topXSorted[i]}/${TOURNAMENT_MULTIPLIER}`)
              let offerMultiplier = (await userOfferMultiplierRef.once('value')).val();
              inboxReward[TOURNAMENT_MULTIPLIER] = offerMultiplier;
              inboxReward[TOURNAMENT_OFFER] = tournamentOffer;
              // console.log(`umair::PlayerID::${topXSorted[i]}::OfferID::${tournamentOffer}::Multiplier::${offerMultiplier}`);
            }
          }
        }
        break;
        case TournamentType.Explorer:
        {
          inboxReward[KEY_EXPLORER_LOOP_ID] = (configs[KEY_EXPLORER_LOOP_ID] === undefined) ? "undefined" : configs[KEY_EXPLORER_LOOP_ID];
          inboxReward[KEY_EXPLORER_CONFIG_VERSION] = (configs[KEY_EXPLORER_CONFIG_VERSION] === undefined) ? "undefined" : configs[KEY_EXPLORER_CONFIG_VERSION];
          inboxReward[KEY_EXPLORER_NAME] = (configs[KEY_EXPLORER_NAME] === undefined) ? "undefined" : configs[KEY_EXPLORER_NAME];
        }
        break;
        default:
        {
        }
        break;
      }
  



      updates[`${common.INBOX_DB_PATH}/${topXSorted[i]}/${tournamentNameKey}`] = inboxReward;
      if (userIDList){
        userIDList += ',';
      }
      userIDList += topXSorted[i]
      count++;
    }
    logString = logString + "**********************Rewards**********************";
    console.log(logString);
    await common.firebaseAdmin.database().ref().update(updates);
  }
  else
  {
    console.log("Tournament::GenerateResults::No users participated in tournament");
  }
  await DDNA.postTournamentResultsEvent(tournamentName, currentSessionID, totalPrize, totalPlayers, userIDList, userPrizeList);

}

async function Umair_ScheduleCloudTask(url, timeInSec, payload, taskName){


  let fullTaskname = common.cloudTasksClient.taskPath(common.PROJECT, common.LOCATION, common.QUEUE, taskName);
  try {
    let parent = common.cloudTasksClient.queuePath(common.PROJECT, common.LOCATION, common.QUEUE)
    let task = {
      httpRequest: {
          httpMethod: 'POST',
          url,
          oidcToken: {
            serviceAccountEmail: common.SERVICE_EMAIL
          },
          body: Buffer.from(JSON.stringify(payload)),
          headers: {
            'Content-Type': 'application/json',
          },
      },
      scheduleTime: {
          seconds: timeInSec
      }
    }
    let [ response ] = await common.cloudTasksClient.createTask({ parent, task })
    console.log(`Tournament::ScheduleCloudTask::Created task:: ${response.name}`); 
    return true;
  }
  catch (error) {
    console.log(`Tournament::ScheduleCloudTask::CreatTaskFailed`); 
    return false;
  }
 
}

function DistributePrize(totalPrize, totalUsers, bracket, topRanks){
  let prizeDistribution = "";
  let prizes = []
  const topRanksSize = topRanks.length
  let distributedPrize = 0
  let topRewardindex=0;
  for(topRewardindex=0 ; topRewardindex < totalUsers && topRewardindex < topRanksSize ; topRewardindex++)
  {
    reward = Math.round(totalPrize * topRanks[topRewardindex]/100)
    distributedPrize+=reward
    prizes[topRewardindex] = reward;
    if (prizeDistribution){
      prizeDistribution += ',';
    }
    prizeDistribution +=  `${topRewardindex+1}:${reward}`; 
  }

  let remainingPlayers = totalUsers - topRewardindex;
  let remainingReward = totalPrize - distributedPrize;
  if (remainingPlayers > 0){
    let totalBuckets = Math.ceil(remainingPlayers/bracket);
    let totalChunks = totalBuckets*(totalBuckets+1)/2;
    let prizePerChunk = Math.floor(remainingReward/totalChunks);
    let prizePerChunkRounded =  prizePerChunk- (prizePerChunk%bracket)
    console.log(`umair::totalBuckets::${totalBuckets}, totalChunks ${totalChunks}, prizePerChunkRounded ${prizePerChunkRounded}`);
    let index = 0;
    for(index=0 ; index < remainingPlayers ; index++)
    {
      let bracketIndex = Math.floor(index/bracket);
      let reward = ((totalBuckets-bracketIndex) * prizePerChunkRounded)/bracket;
      prizes[topRewardindex + index] = reward;
    }  

    let bracketIndex = 0;
    for(bracketIndex=0 ; bracketIndex < totalBuckets ; bracketIndex++)
    {
      let reward = ((totalBuckets-bracketIndex) * prizePerChunkRounded)/bracket;
      let startingIndex =  topRanksSize+1+ bracketIndex*bracket;
      let endingIndex =  startingIndex+bracket-1;
      prizeDistribution +=  `,${startingIndex}-${endingIndex}:${reward}`; 
    }  
    console.log(`umair::distrinutionString::${prizeDistribution}`);


  }
  return {
    prizes, 
    prizeDistribution
  }
}

module.exports = {
  Cloud_StartTournament,
  Cloud_StopTournament,
  Cloud_CalculateResults,
  SetupDefaultTournament,
  SetupExplorerTournament,
}
