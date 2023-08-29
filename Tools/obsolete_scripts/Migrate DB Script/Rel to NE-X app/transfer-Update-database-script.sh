CURRENT_DIR="$( dirname "$0" )"


appToBeExportedDBURI='mongodb://heroku_7fhw0vgd:2nm2q97m0terqkhs85en2lf860@ds015194.mlab.com:15194/heroku_7fhw0vgd' #e.g release app DB URL
appNeedsImportingDBURI='mongodb://heroku_d7qwz30c:t8cet72bkoehet07g9fdtjmbkj@ds023054.mlab.com:23054/heroku_d7qwz30c' #e.g NE-X DB URL

credentialsString=$(echo $appToBeExportedDBURI| cut -d':' -f3-4)
passwordString=$(echo $credentialsString| cut -d'@' -f1)
userNameString=$(echo $credentialsString| cut -d'/' -f2)
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