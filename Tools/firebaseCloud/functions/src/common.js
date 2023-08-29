const functions = require('firebase-functions');
const CLOUD_TASK  = require('@google-cloud/tasks');
const firebaseAdmin = require('firebase-admin');


const OTHER_CONFIGS = require("../res/TournamentConfigs.json")

const PROJECT = JSON.parse(process.env.FIREBASE_CONFIG).projectId
const DATABASE_URL = `https://${PROJECT}.firebaseio.com`
const TOURNAMENT_DB_PATH = 'tournaments';
const TOURNAMENT_STATUS_NODE = 'status';
const TOURNAMENT_END_TIME_NODE = 'end_time';
const TOURNAMENT_CURRENT_STATE_NODE = 'current_state';
const TOURNAMENT_SESSION_NODE = 'session';

const INBOX_DB_PATH = 'reward_inbox';
const TOURNAMENT_LEADERBOARD_PATH =  'leaderboard';
const TOURNAMENT_LEADERBOARD_SCORE_NODE =  'scores';
const LOCATION = 'us-central1'
const QUEUE = 'tournamentQueue'
const TOTAL_PLAYER = 'total_players'
const COINS_WAGERED = 'coins_wagered'
const SERVICE_EMAIL = OTHER_CONFIGS.service_account
const DELTADNA_ENVIRONMENT_KEY = OTHER_CONFIGS.DELTADNA_ENVIRONMENT_KEY
const DELTADNA_COLLECT_URL = OTHER_CONFIGS.DELTADNA_COLLECT_URL
// const SERVICE_EMAIL = "cloudfunctioninvoker@cleopetra-slots-36468229.iam.gserviceaccount.com"
const USERS_DB_PATH = 'users';
const Parse_URL = OTHER_CONFIGS.Parse_URL;
const PARSE_APP_NAME = OTHER_CONFIGS.PARSE_APP_NAME;

const  TournamentStatus = {
  STOPED: 0,
  WAITING : 1,
  RUNNING : 2,
  PREPARING_RESULTS : 3
}


firebaseAdmin.initializeApp();  

const cloudTasksClient = new CLOUD_TASK.CloudTasksClient();



const FUNCTION_WAITING_RESULT = 'Cloud_CalculateResults';
const FUNCTION_START_TOURNAMENT = 'Cloud_StartTournament';
const FUNCTION_STOP_TOURNAMENT = 'Cloud_StopTournament';

module.exports = {
  firebaseAdmin,
  cloudTasksClient,
  PROJECT,
  LOCATION,
  QUEUE,
  SERVICE_EMAIL,
  TOURNAMENT_DB_PATH,
  TOURNAMENT_LEADERBOARD_PATH,
  TOTAL_PLAYER,
  COINS_WAGERED,
  INBOX_DB_PATH,
  TOURNAMENT_END_TIME_NODE,
  TOURNAMENT_SESSION_NODE,
  TOURNAMENT_STATUS_NODE,
  TournamentStatus,
  TOURNAMENT_LEADERBOARD_SCORE_NODE,
  TOURNAMENT_CURRENT_STATE_NODE,
  DELTADNA_COLLECT_URL,
  DELTADNA_ENVIRONMENT_KEY,
  Parse_URL,
  USERS_DB_PATH,
  PARSE_APP_NAME,
  FUNCTION_WAITING_RESULT,
  FUNCTION_START_TOURNAMENT,
  FUNCTION_STOP_TOURNAMENT
}


