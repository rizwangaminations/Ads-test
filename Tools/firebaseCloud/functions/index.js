const functions = require('firebase-functions');
const PROJECT = JSON.parse(process.env.FIREBASE_CONFIG).projectId

const leaderboardHandler = require('./src/leaderboard');
const tournaments = require('./src/tournaments');
const testFunctions = require('./src/testFunctions');



const runtimeOptsHigh = {
  timeoutSeconds: 360,
  memory: '1GB'
}

const runtimeOptsMedium = {
  timeoutSeconds: 360,
  memory: '512MB'
}



//Leaderboard
exports.completeDay = functions.runWith(runtimeOptsHigh).https.onRequest(leaderboardHandler.completeDayFunc);
exports.resetTodayLeaderboard = functions.runWith(runtimeOptsHigh).pubsub.schedule('every day 00:00').onRun(leaderboardHandler.resetLeaderboard);

//Tournamnets
// exports.startTournamentSession = functions.runWith(runtimeOptsMedium).https.onRequest(tournaments.startTournamentSessionFunc);
// https://us-central1-cleopetra-slots-36468229.cloudfunctions.net/startTournamentSession?tournament=global&delay=30

// exports.internal_startTournament = functions.runWith(runtimeOptsMedium).https.onRequest(tournaments.startTournamentFunc);
// exports.internal_stopTournament = functions.runWith(runtimeOptsMedium).https.onRequest(tournaments.stopTournamentFunc);
// exports.internal_calculateResults = functions.runWith(runtimeOptsMedium).https.onRequest(tournaments.calculateResultsFunc);
exports.Cloud_StartTournament = functions.runWith(runtimeOptsMedium).https.onRequest(tournaments.Cloud_StartTournament);
exports.Cloud_StopTournament = functions.runWith(runtimeOptsMedium).https.onRequest(tournaments.Cloud_StopTournament);
exports.Cloud_CalculateResults = functions.runWith(runtimeOptsMedium).https.onRequest(tournaments.Cloud_CalculateResults);
exports.SetupDefaultTournament = functions.runWith(runtimeOptsMedium).https.onRequest(tournaments.SetupDefaultTournament);
exports.SetupExplorerTournament = functions.runWith(runtimeOptsMedium).https.onRequest(tournaments.SetupExplorerTournament);



//Test Functions
// exports.postUser = functions.runWith(runtimeOptsMedium).https.onRequest(testFunctions.postUserFunc);
exports.postMultipleUsers = functions.runWith(runtimeOptsMedium).https.onRequest(testFunctions.postMultipleUsersFunc);
// exports.autoPostUsers = functions.runWith(runtimeOptsMedium).pubsub.schedule('every 1 minutes').onRun(testFunctions.autoPostUsersFunc);

exports.showCloudTasks = functions.runWith(runtimeOptsMedium).https.onRequest(testFunctions.showCloudTasks);


