CURRENT_DIR="$( dirname "$0" )"

appToBeExportedDBURI='mongodb://heroku_tdn9jtkk:k09hdljpdmek2qqifrl3p2tm7h@ds033846-a0.mlab.com:33846,ds033846-a1.mlab.com:33846/heroku_tdn9jtkk?replicaSet=rs-ds033846' #e.g develop app DB URL
appNeedsImportingDBURI='mongodb://heroku_csb67h8q:nab35oj6l6sibicciilfr9c7lr@ds043002.mlab.com:43002/heroku_csb67h8q' #e.g release app DB URL

credentialsString=$(echo $appToBeExportedDBURI| cut -d':' -f3-4)
passwordString=$(echo $credentialsString| cut -d'@' -f1)
#userNameString=$(echo $credentialsString| cut -d'/' -f2)
userNameString=${appToBeExportedDBURI:10:15}
urlString=$(echo $credentialsString| cut -d'@' -f2)
finalURLString=$(echo $urlString| cut -d'/' -f1)

dbToExportURI=$finalURLString
dbToExportUserName=$userNameString
dbToExportPassword=$passwordString

credentialsString=$(echo $appNeedsImportingDBURI| cut -d':' -f3-4)
passwordString=$(echo $credentialsString| cut -d'@' -f1)
userNameString=$(echo $credentialsString| cut -d'/' -f2)
urlString=$(echo $credentialsString| cut -d'@' -f2)
finalURLString=$(echo $urlString| cut -d'/' -f1)

dbNeedsImportingURI=$finalURLString
dbNeedsImportingUserName=$userNameString
dbNeedsImportingPassword=$passwordString


INSTALL_DIR="${CURRENT_DIR}/dump/"$dbToExportUserName
echo "Dumping DB to path: " $INSTALL_DIR

mongodump -h $dbToExportURI -d $dbToExportUserName -u $dbToExportUserName -p $dbToExportPassword -o "${CURRENT_DIR}/dump/"

echo -----Exporting completed-----


echo -----Importing db dump-----

echo "Importing DB from path: " $INSTALL_DIR
mongorestore -h $dbNeedsImportingURI -d $dbNeedsImportingUserName -u $dbNeedsImportingUserName -p $dbNeedsImportingPassword "${INSTALL_DIR}"

echo -----Importing db completed-----


echo -----Update database-----
echo "Reading update parse database python script from path: " "${CURRENT_DIR}/update_mongo.py"
python "${CURRENT_DIR}/update_parse_db.py" $appNeedsImportingDBURI $userNameString
