#!/bin/sh
SCRIPT_DIR="$( dirname "$0" )"

# dirList="$SCRIPT_DIR/../proj.ios_mac/ios"
# ,$SCRIPT_DIR/../bonusgameengine,$SCRIPT_DIR/../modulecommon"
# $SCRIPT_DIR/../moduleinapppurchase,
dirList="$SCRIPT_DIR/../proj.ios_mac/ios,$SCRIPT_DIR/../moduleinapppurchase,$SCRIPT_DIR/../Classes,$SCRIPT_DIR/../SlotEngine,$SCRIPT_DIR/../bonusgameblackred,$SCRIPT_DIR/../bonusgamemagilair,$SCRIPT_DIR/../bonusgamepickanobject,$SCRIPT_DIR/../moduleanalytics,$SCRIPT_DIR/../moduleconfigurationstorage,$SCRIPT_DIR/../modulefacebook,$SCRIPT_DIR/../moduleinstallationdetection,$SCRIPT_DIR/../modulelocalnotification,$SCRIPT_DIR/../modulexplatformshare,$SCRIPT_DIR/../modulecommon,$SCRIPT_DIR/../bonusgameengine,$SCRIPT_DIR/../moduleads"

ignoreList="$SCRIPT_DIR/../SlotEngine/Utility,$SCRIPT_DIR/../moduleanalytics/cpp/ThirdParty,$SCRIPT_DIR/../modulecommon/cpp/ThirdParty,$SCRIPT_DIR/../bonusgameblackred/wp8.1,$SCRIPT_DIR/../bonusgamemagilair/wp8.1,$SCRIPT_DIR/../bonusgamepickanobject/wp8.1,$SCRIPT_DIR/../moduleanalytics/wp8.1,$SCRIPT_DIR/../moduleconfigurationstorage/wp8.1,$SCRIPT_DIR/../moduleinstallationdetection/wp8.1,$SCRIPT_DIR/../modulelocalnotification/wp8.1,$SCRIPT_DIR/../modulecommon/android,$SCRIPT_DIR/../bonusgameengine/wp8.1,$SCRIPT_DIR/../moduleads/wp8.1,$SCRIPT_DIR/../moduleinapppurchase/wp8.1,$SCRIPT_DIR/../modulefacebook/wp8.1,$SCRIPT_DIR/../modulecommon/wp8.1,$SCRIPT_DIR/../modulecommon/ios/SDK,$SCRIPT_DIR/../modulecommon/cpp/ThirdParty/NDKHelper/"
python "$SCRIPT_DIR/stringObfuscator.py" --dir=$dirList --ignoreDir=$ignoreList
# python "$SCRIPT_DIR/FileToStrings.py" --dir=$dirList --ignoreDir=$ignoreList
# echo "Strings obfuscated"
