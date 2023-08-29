const common = require('./common');
const DDNA = require('./DDNA');


const postUserFunc = async (req, res) => {
  var tournamentName = (req.query.tournament || req.body.tournament)
  var userID = (req.query.userID || req.body.userID)
  var score = (req.query.score || req.body.score)
  console.log("umair::postUserFunc::started");
  await postUser(tournamentName, userID, score)
  console.log("umair::postUserFunc::ended");
  res.sendStatus(200);
};


const postMultipleUsersFunc = async (req, res) => {

  var tournamentName = (req.query.tournament || req.body.tournament || 'global')
  var count = (req.query.count || req.body.count || 20)
  console.log("umair::postMultipleUsersFunc::started");
  await postMultipleUsers(tournamentName, count)
  console.log("umair::postMultipleUsersFunc::ended");
  res.sendStatus(200);
};


async function postMultipleUsers(tournamentName, pCount) {
  try {
    var statusNodePath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_STATUS_NODE}`; 
    var statusSnap = await (await common.firebaseAdmin.database().ref(statusNodePath).once('value')).val()
    if (statusSnap === common.TournamentStatus.RUNNING){
      var sessionID = await common.firebaseAdmin.database().ref(`${common.TOURNAMENT_DB_PATH}/${tournamentName}/${common.TOURNAMENT_CURRENT_STATE_NODE}/${common.TOURNAMENT_SESSION_NODE}`).once('value')
      var currentSessionID =  (sessionID.val() || 1);

      var countRefPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/${common.TOURNAMENT_LEADERBOARD_PATH}/${currentSessionID}/${common.TOTAL_PLAYER}`; 
      var snap = await common.firebaseAdmin.database().ref(countRefPath).once('value')
      var currentPlayerCount =  (snap.val() || 0);
      var max = 100000;
      var min = 10;
      for (var i = 1; i <= pCount; i++) {
        var score = Math.floor(Math.random() * (max - min) ) + min;
        await postUser(tournamentName, currentSessionID, "Player-" + (currentPlayerCount+i), score);
      }
      await common.firebaseAdmin.database().ref(countRefPath).transaction((current) => {
        return (parseInt(current || 0) + parseInt(pCount));
      });
  
      
    }
  } catch (error) {
    console.error('Unable to get template');
    console.error(error);
    return null;
  }
};



async function postUser(tournamentName, currentSessionID, userID, score) {
  try {
    var playerScore = {score}
    var leaderboardPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/${common.TOURNAMENT_LEADERBOARD_PATH}/${currentSessionID}/${common.TOURNAMENT_LEADERBOARD_SCORE_NODE}`;
    var leaderboardRef = common.firebaseAdmin.database().ref(leaderboardPath);
    await leaderboardRef.child(userID).set(playerScore);
    var coinsWageredPath = `${common.TOURNAMENT_DB_PATH}/${tournamentName}/${common.COINS_WAGERED}`;
    var coinsWageredRef = common.firebaseAdmin.database().ref(coinsWageredPath);
    coinsWageredRef.transaction((current) => {
      return (current || 0) + score;
    });
    return null;
  } catch (error) {
    console.error('Unable to get template');
    console.error(error);
    return null;
  }
};

const autoPostUsersFunc = async context => {
  var tournamentName = 'global'
  var count = 20
  console.log("umair::postMultipleUsersFunc::started");
  await postMultipleUsers(tournamentName, count)
  console.log("umair::postMultipleUsersFunc::ended");

  return null;
};

const showCloudTasks = async (req, res) => {

  
  let parent = common.cloudTasksClient.queuePath(common.PROJECT, common.LOCATION, common.QUEUE);
  let request = {
    parent : parent.toString(),
    responseView :  2
  };
  let httpMessage = "";
  httpMessage +=  "<h2>Running Tournaments</h2>";
  httpMessage +=  "<dl>";


  let currentTimeStamp = parseInt(Date.now()/1000);

  httpMessage += `<dt>Current Time: ${currentTimeStamp}</dt>`

  let [tasksList]  = await common.cloudTasksClient.listTasks(request);
  if (tasksList)
  {
    for (let task of tasksList) {
      

      let bodyString = task.httpRequest.body.toString();
      // console.log("umair::BODYSTRING::"+bodyString);
      let taskJSON = JSON.parse(bodyString);
      let configs = taskJSON.configs;
      let delay = configs.delay;
      let duration = configs.duration;
      let resultTime = configs.resultTime;
      let name = configs.name;
      let parse = configs.parse;

      let endTime = parseInt(task.scheduleTime.seconds);
      let functionName = task.httpRequest.url.split('/').pop();

      let currentState = "Preparing Result";

      if (functionName == common.FUNCTION_START_TOURNAMENT)
      {
        endTime += duration;
        endTime += resultTime;
        currentState = "Waiting"
      }
      if (functionName == common.FUNCTION_STOP_TOURNAMENT)
      {
        endTime += resultTime;
        currentState = "Running"
      }
      let cycleLenth =  delay + duration + resultTime;
      httpMessage += `<dt>${name}</dt>`
        httpMessage += `<dd> CurrentState: ${currentState}</dd>`
        httpMessage += `<dd> End Time: ${endTime}</dd>`
        httpMessage += `<dd> Parse: ${parse}</dd>`
        httpMessage += `<dd> Cycle Time: ${cycleLenth}</dd>`
    
    }
  }
  else
  {
    console.log("umair::tasksListNull");

  }

  httpMessage +=  "</dl>";
  res.status(200).send(httpMessage);
};

module.exports = {
  postUserFunc,
  postMultipleUsersFunc,
  autoPostUsersFunc,
  showCloudTasks
}