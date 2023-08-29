from pymongo import MongoClient
import json
import argparse
import os
from pprint import pprint

def run():
    print("Opening mongodb client")
    parser = argparse.ArgumentParser()
    parser.add_argument("appDbURI", help="Database URI", type=str)
    parser.add_argument("username", help="UserName", type=str)
    args = parser.parse_args()
    
    client = MongoClient(args.appDbURI)

    db = client[args.username]

    print("Step1: Cleaning the leaderboard data")
    leaderboardData = db["Leaderboard"]
    result = leaderboardData.delete_many({})

    print("Step2: Cleaning the levels data except first 4")
    levelData = db["Levels"]
    cursor = levelData.remove({"level": {"$gt": 3}})

    print("Step3: Reading and updating parse from the input configurations")
    inputConfigPath = os.path.dirname(os.path.abspath(__file__)) + "/input-config.json"
    with open(inputConfigPath) as data_file:
        jsonConfigData = json.load(data_file)


    print(" Step3a: Updating in-app-puchase table on parse")
    update_inapp_table_on_parse(db, jsonConfigData, "InAppPurchase")

    print(" Step3b: Updating platform share urls on parse")
    update_table_on_parse(db, jsonConfigData, "M_XPlatformShare", "ShareURL")

    print(" Step3c: Updating platforms version on parse")
    update_table_on_parse(db, jsonConfigData, "UpdateVersion", "Version")

    #print "Step3d: Updating in-app-promo IAP-IDS on parse"
    #update_inapp_promo_on_parse(db) this is not needed as objects id are also same in in-app purchase parse table
    #print "Step3d: Done"

    print("Step3: Completed")

def update_inapp_table_on_parse(db, configData, tableName):
    
    tableData = db[tableName]
    
    iosPlatformPackage = configData[tableName]["iOS"]
    androidPlatformPackage = configData[tableName]["Android"]
    amazonPlatformPackage = configData[tableName]["Amazon"]
    wpPlatformPackage = configData[tableName]["WP8"]
    
    identifiers = configData[tableName]["identifiers"]
    i = 1
    j = 1
    for identifier in identifiers:
        platformIAPJson = { "ProductID_IOS": iosPlatformPackage + "." +identifier, "ProductID_Android": androidPlatformPackage + "." +identifier,"ProductID_Amazon": amazonPlatformPackage + "." +identifier, "ProductID_WP": wpPlatformPackage + "." +identifier}
        iosOldInAppIdentifier = "com.megarama.newengine1.CoinPack" + str(i)
        
        if j%2 == 0:
            i+=1
        j+=1
        
        toFind = {"ProductID_IOS": iosOldInAppIdentifier}
        newJsonToSet = { "$set": platformIAPJson, "$currentDate": {"lastModified": True}}
        result = tableData.update_one(toFind, newJsonToSet)

def update_table_on_parse(db, configData, tableName, columnName):
    tableData = db[tableName]
    update_column("iOS", configData[tableName]["iOS"], tableData, columnName)
    update_column("Android",configData[tableName]["Android"], tableData, columnName)
    update_column("Amazon",configData[tableName]["Amazon"], tableData, columnName)
    windowPhoneColumnValue = "WP8"
    if (tableName == "UpdateVersion"):
        update_column("All",configData[tableName][windowPhoneColumnValue], tableData, columnName)
        windowPhoneColumnValue = "Wp"
    update_column(windowPhoneColumnValue,configData[tableName]["WP8"], tableData, columnName)

def update_column(platform, newValue, parseTable, columnName):
    toFind = {columnName: platform}
    newJsonToSet = { "$set": { columnName: newValue}, "$currentDate": {"lastModified": True}}
    result = parseTable.update_one(toFind, newJsonToSet)

def update_inapp_promo_on_parse(db):
    tableData = db["InAppPurchase"]
    toFindQuery1 = {"ProductID_IOS": "com.megarama1.newengine1.CoinPack1", "RewardType": "coins"}
    toFindQuery2 = {"ProductID_IOS": "com.megarama1.newengine1.CoinPack6", "RewardType": "coins"}
    resultQuery1 = tableData.find_one(toFindQuery1)
    resultQuery2 = tableData.find_one(toFindQuery2)
    iAPId1 = resultQuery1["_id"]
    iAPId2 = resultQuery2["_id"]
    
    tableData = db["IAPPromo"]
    newJsonToSet = { "$set": { "IAP1": iAPId1}, "$currentDate": {"lastModified": True}}
    tableData.update_many({}, newJsonToSet)

    newJsonToSet = { "$set": { "IAP2": iAPId2}, "$currentDate": {"lastModified": True}}
    tableData.update_many({}, newJsonToSet)

# -- RUN -- #
run()