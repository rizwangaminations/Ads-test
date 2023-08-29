#!/bin/sh
SCRIPT_DIR="$( dirname "$0" )"
FilePathFB=$SCRIPT_DIR/../../modulecommon/cpp/GameCommonSettings.cpp
FilePathMax=$SCRIPT_DIR/../../moduleads/ios/networks/AppLovinNetwork.mm

sed -i '' "s~, m_isFBFriendsEnabled(false).*~, m_isFBFriendsEnabled(true)~g" $FilePathFB
sed -i '' "s~m_isFBFriendsEnabled =.*~\/\/m_isFBFriendsEnabled = data[(\"FBFriendEnabled\")].asBool();~g" $FilePathFB


sed -i '' "s~\[sdk showMediationDebugger\];.*~\/\/[sdk showMediationDebugger];~g" $FilePathMax


sed -i '' "s~m_isForcedFreeSpinEnabled           =.*~\/\/m_isForcedFreeSpinEnabled           = data\[(\"ForceFreeSpin\")\]                \.asBool();~g" $FilePathFB

echo "FB Review build settings applied"