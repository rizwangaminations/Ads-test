
const common = require('./common');


const completeDayFunc = async (req, res) => {
  console.log("completeDay", "STARTED");
  var status1 = await resetLeaderboardToday("leaderboards/coins");
  var status2 = await resetLeaderboardToday("leaderboards/levels");
  var status3 = await resetLeaderboardToday("leaderboards/wins");
  console.log("completeDay", "Ended");
  res.status(200).send("umair done: " +status1+status2+status3);
};



const resetLeaderboard = async context => {
  console.log('resetTodayLeaderboard',"Started");
  var status1 = await resetLeaderboardToday("leaderboards/coins");
  var status2 = await resetLeaderboardToday("leaderboards/levels");
  var status3 = await resetLeaderboardToday("leaderboards/wins");
  console.log("resetTodayLeaderboard", "Ended Callback::"+status1+status2+status3);
  return null;
};

async function resetLeaderboardToday(leaderboard_path) {
  try{
    console.log("resetLeaderboardToday", "STARTED");
    var today_ref = common.firebaseAdmin.database().ref(leaderboard_path+'/today');
    var yesterday_ref = common.firebaseAdmin.database().ref(leaderboard_path+'/yesterday');
    return moveRecord(today_ref,yesterday_ref);
  }
  catch (error){
    console.error("resetLeaderboardToday", "Error::",error);
    return error;
  }
}

async function moveRecord(oldRef, newRef) {   
  try {
    var snap = await oldRef.once('value');
    await newRef.set(snap.val());
    await oldRef.set(null);
    console.log('Done!');
    return 'success';
  }catch(err) {
       console.log(err.message);
       return err.message;
  }
}


module.exports = {
  completeDayFunc,
  resetLeaderboard,
}

