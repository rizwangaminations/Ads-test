//
//  CommonModule.h
//  ModuleCommon
//
//  Created by Muhammad Arslan on 15/08/2015.
//  Copyright (c) 2015 Gaminations. All rights reserved.
//

#ifndef CommonModule_h__
#define CommonModule_h__

#include "CommonModuleConstants.h"
#include "cocos2d.h"

using namespace cocos2d;

class ___CommonModule___
{
private:
    long long m_gameInstallTimeStamp;
    EventListenerCustom* m_releaseCachedResourcesObserver;
    static ___CommonModule___* m_instance;
    std::vector<Texture2D*> m_retainedTextures;
    std::vector<SpriteFrame*> m_retainedSpriteFrames;
    bool m_didReceiveMemoryWarning;
    std::vector<std::string> m_mainMenuResources;
    std::vector<std::string> m_levelResources;
    bool m_isInternetConnected;
    std::string m_currencyCode;
    std::string m_gameSettingsConfigName;

private:
    ___CommonModule___();
    virtual ~___CommonModule___();

    static ___CommonModule___* getInstance();
    static void ___destroyInstance___();
    virtual bool init();

    static void ___addSearchPath___();
    static void ___setupLocalization___();
    static void ___setupEasyNDK___();
    void ___initializeFirebase___();
    void ___configureGameInstallTime___();
    void ___imageLoadedCallback___(Texture2D* texture);

public:
    static void ___initialize___();
    static void ___preLoadMainMenuGraphicsAsync___();
    static void ___preLoadMainMenuGraphics___();
    static void ___preLoadLevelGraphics___();
    static void ___unloadLevelGraphics___();
    static bool ___isVersionCompatible___(const std::string& minVersionToCompare, const std::string& maxVersionToCompare);
    static bool ___isDateCompatible___(const std::string& dateStartToCompare, const std::string& dateEndToCompare);
    static const std::string ___getVersion___();
    static void ___releaseCachedResources___();
    static void ___removeUnusedResources___();
    static void ___reloadSpriteFrames___();

    static long long ___getGameInstallTime___();
    static bool ___isFreeCoinsButtonNeeded___();
    static bool ___isAutoDownloadEnabled___();
    static bool ___isAchievementSystemEnabled___();
    static bool ___isAchievementCompletePopupEnabled___();
    static bool ___isForcedFreeSpinEnabled___();
    static bool ___useFileServer___();
    static bool ___useNativeTextures___();
    static bool ___useLevelButtonBundles___();
    static bool ___isSecondaryCurrencyEnabled___();
    static int ___getDaysPassedFromInstallation___();
    static void ___setWritablePath___(const std::string& path);
    static const std::string& ___getMoreGamesPath___();
    static const std::string& ___getFBMessengerPath___();
    static const std::string& ___getTermsAndConditionsPath___();
    static const std::string& ___getPrivacyPolicyPath___();
    static const std::string& ___getFileServerPath___();
    static bool ___isRankSystemEnabled___();
    static bool ___isPiggyBankEnabled___();
    static bool ___isVIPSystemEnabled___();
    static bool ___postValidIAPEventsToFB___();
    static bool ___isSubscriptionEnabled___();
    static bool ___isDailyBonusEnabled___();
    static bool ___isQuestEnabled___();
    static bool ___isLeaderboardEnabled___();
    static bool ___isFBFriendsEnabled___();
    static bool ___isGambleEnabled___();
    static bool ___isIAPEnabled___();
    static bool ___isShopButtonEnabled___();
    static bool ___isDailyMissionsEnabled___();
    static bool ___isExplorerMissionsEnabled___();
    static bool ___isATTFeatureEnabled___();
    static bool ___isQADevice___(const std::string& deviceUniqueIdentifier);
    static std::set<int>& ___getLevelAchievedEventList___();
    static std::string& ___getActiveTournamentsString___();
    static float ___getVipMultiplier___();
    static int ___getRankSystemSpinCountMin___();
    static int ___getRankSystemSpinCountMax___();
    static int ___getCollectFromShopTimer___();
    static int ___getLeaderboardRefreshTime___();
    static int ___getTournamentRewardExpireTime___();
    static int ___getPromoEngagementTimeout___();
    static int ___getMaxConcurrentTransfers___();
    static int ___getLevelButtonGapSize___();
    static int ___getCloudPostTime___();
    static int ___getSpinsSteps___();
    static int ___getSpinsToTrack___();
    static const std::string& ___getShopAssetName___();
    static const std::string& ___getMiniShopAssetName___();
    static const void ___setShopAssetName___(const std::string& shopAssetName);
    static const void ___setMiniShopAssetName___(const std::string& miniShopAssetName);
    static const void ___setGameSettingsConfigName___(const std::string& gameSettingsConfigName);
    static std::string& ___getGameSettingsConfigName___();
    static const std::string& ___getUIParametersPrefix___();
    static bool ___isLevelButtonGapSizeConfigured___();
    static double ___getFreeCoinsAmount___();
    static double ___evaluateExpression___(const std::string expression);
    static inline bool ___getDidReceiveMemoryWarning___() { return ___CommonModule___::getInstance()->m_didReceiveMemoryWarning; }
    static inline void ___setDidReceiveMemoryWarning___(bool memoryWarningValue) {
        ___CommonModule___::getInstance()->m_didReceiveMemoryWarning = memoryWarningValue;
    }
    static const std::string& ___getNativeiOSRateVersionsJson___();
    static const std::string& ___getMainMenuBonusGameId___();
    static const std::string& ___getDailyBonusGameId___();
    static inline bool ___isEnableAds___()
    {
        return true;
    }
    
#if CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID
    static inline bool ___getIsInternetConnected___() { return ___CommonModule___::getInstance()->m_isInternetConnected; }
#endif
    void ___onInternetConnectivityChange___(Node *sender, cocos2d::Value data);
};

#endif // CommonModule_h__
