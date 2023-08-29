const common = require('./common');
var rp = require('request-promise');


var envKey = common.DELTADNA_ENVIRONMENT_KEY;
var collectURL = common.DELTADNA_COLLECT_URL;
var url = collectURL + '/' + envKey + '/bulk';
var userID = "";
var eventList = [];


async function postTournamentStartEvent(tournament, sessionID) {
  recordEvent({
    eventName: 'tournamentSetup',
    eventParams: {
      tournamentID: tournament,
      tournamentSession: sessionID
    }
  });
  await postAnalytics()
}

async function postTournamentResultsEvent(tournament,sessionID,  totalPrize, totalUsers, users, prize) {
  recordEvent({
    eventName: 'tournamentResults',
    eventParams: {
      tournamentID: tournament,
      tournamentSession: sessionID,
      prizeTotal: totalPrize,
      totalUsers: totalUsers,
      // usersLeaderboard: users,
      prizeDistribution: prize
    }
  });
  await postAnalytics()
}




async function postAnalytics() {

  if (eventList.length == 0) {
    console.log('DDNA::No events to send');
    return;
  }
  var recordedEvents = eventList;
  eventList = [];

  try {
    var options = {
      uri: url,
      method: 'POST',
      headers: {
        "Content-Type": "application/json"
      },
      body: {
        eventList: recordedEvents
      },
      json: true 
    };

    rp(options).then(function (parsedBody) {
        // POST succeeded...
        console.log("DDNA::postSuccess::"+parsedBody);
    })
    .catch(function (err) {
        console.log("DDNA::postFailed::"+ err.toString());
    });

  } catch (error) {
    console.error('DDNA::Unable to get template');
    console.error(error);
  }
};

function recordEvent(event) {
  //fetch the default event parameters and copy this to the event to record
  event = extend(true, getDefaults(), event);
  eventList.push(event);
  console.log("DDNA::Recording event");
  console.log(JSON.stringify(event));
}

var extend = function () {

	// Variables
	var extended = {};
	var deep = false;
	var i = 0;
	var length = arguments.length;

	// Check if a deep merge
	if ( Object.prototype.toString.call( arguments[0] ) === '[object Boolean]' ) {
		deep = arguments[0];
		i++;
	}

	// Merge the object into the extended object
	var merge = function (obj) {
		for ( var prop in obj ) {
			if ( Object.prototype.hasOwnProperty.call( obj, prop ) ) {
				// If deep merge and property is an object, merge properties
				if ( deep && Object.prototype.toString.call(obj[prop]) === '[object Object]' ) {
					extended[prop] = extend( true, extended[prop], obj[prop] );
				} else {
					extended[prop] = obj[prop];
				}
			}
		}
	};

	// Loop through each object and conduct a merge
	for ( ; i < length; i++ ) {
		var obj = arguments[i];
		merge(obj);
	}

	return extended;

};

function getDefaults() {
  return {
    userID: getUser(),
    eventTimestamp: getTimestamp(),
    eventParams: {
      platform: 'WEB'
    }
  };
}

function getUser() {
  return "firebase";
}

function getTimestamp() {
  //return a timestamp in the format 2016-03-01 20:26:50.148 and in UTC
  var d = new Date();
  return d.getUTCFullYear() +
    '-' + (d.getUTCMonth() + 1) + '-' + d.getUTCDate() +
    ' ' + d.getUTCHours() + ':' + d.getUTCMinutes() +
    ':' + d.getUTCSeconds() + '.' + d.getUTCMilliseconds();
}

module.exports = {
  postAnalytics,
  postTournamentStartEvent,
  postTournamentResultsEvent,
}
