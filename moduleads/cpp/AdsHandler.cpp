//
//  AdsHandler.cpp
//  ModuleAds
//
//  Created by Abdul Wasay on 17/08/2015.
//  Copyright (c) 2015 Gaminations. All rights reserved.
//

#include "AdsHandler.h"
#include "ThirdParty/NDKHelper/NDKHelper/NDKHelper.h"
#include "ModuleAdsConstants.h"
#include "AppOpenAdManager.h"
#include "CommonModule.h"

#if CC_TARGET_PLATFORM == CC_PLATFORM_IOS
#include "ModuleAdsBridge.h"
#endif

#define REWARDED_VIDEO_LIMIT_MODEL_KEY ("Rewarded Video")
#define REWARDED_VIDEO_LOGGED_DATE_PREFIX ("REWARDED_VIDEO_LOGGED_DATE_")

#define PLACEMENT_ADS_LIMIT_MODEL_KEY ("Placement Ads")
#define PLACEMENT_ADS_LOGGED_DATE_PREFIX ("PLACEMENT_ADS_LOGGED_DATE_")

#define BANNER_ADS_LIMIT_MODEL_KEY ("Banner Ads")

#define APP_OPEN_ADS_LIMIT_MODEL_KEY ("AppOpen Ads")
#define APP_OPEN_ADS_LOGGED_DATE_PREFIX ("APP_OPEN_ADS_LOGGED_DATE_")

#define REMOVE_ACTION_TAG 1

static ___AdsHandler___ *m_instance = nullptr;

/*static*/ ___AdsHandler___* ___AdsHandler___::___getInstance___()
{
    if (!m_instance)
    {
        m_instance = new ___AdsHandler___();
        CCASSERT(m_instance, "FATAL: Not enough memory");
        m_instance->___init___();
    }
    
    return m_instance;
}

void ___AdsHandler___::___destroyInstance___()
{
    delete m_instance;
    m_instance = nullptr;
}

bool ___AdsHandler___::___init___()
{
    NDKHelper::addSelector(MODULE_ADS_NDK_GROUP_NAME, ("setAdsCacheStatus"), CC_CALLBACK_2(___AdsHandler___::___setAdsCacheStatus___, this), nullptr);
    NDKHelper::addSelector(MODULE_ADS_NDK_GROUP_NAME, ("adClosedCallback"), CC_CALLBACK_2(___AdsHandler___::___adClosedCallback___, this), nullptr);
    NDKHelper::addSelector(MODULE_ADS_NDK_GROUP_NAME, ("adStartedCallback"), CC_CALLBACK_2(___AdsHandler___::___adStartedCallback___, this), nullptr);
    NDKHelper::addSelector(MODULE_ADS_NDK_GROUP_NAME, ("adFailedCallback"), CC_CALLBACK_2(___AdsHandler___::___adFailedCallback___, this), nullptr);
    NDKHelper::addSelector(MODULE_ADS_NDK_GROUP_NAME, ("sendGameAnalyticsWarning"), CC_CALLBACK_2(___AdsHandler___::___sendGameAnalyticsWarning___, this), nullptr);
    NDKHelper::addSelector(MODULE_ADS_NDK_GROUP_NAME, ("onAdsSDKInitializedCallback"),
                           CC_CALLBACK_2(___AdsHandler___::___onAdsSDKInitializedCallback___, this), nullptr);
    
    
    auto eventDispatcher = cocos2d::Director::getInstance()->getEventDispatcher();
    
    auto backgroundListener = EventListenerCustom::create(ADS_LIMIT_SESSION_ENDED, [this](EventCustom* event)
      {
          this->___onAdsLimitSessionEndedEvent___();
      });
    eventDispatcher->addEventListenerWithFixedPriority(backgroundListener, 1);
    return true;
}

___AdsHandler___::___AdsHandler___()
:   m_isParsingDone(false)
,   m_isAdsSDKFinishedInitilisation(false)
,   m_offersCountInSession(0)
,   m_rewardedVideoCountInSession(0)
,   m_placementAdsCountInSession(0)
,   m_loadingLayer(nullptr)
,   m_currentDisplayedBannerNetwork((""))
,   m_lastAdRequester((""))
,   m_networkName(("applovin"))
,   m_adNetwork(make_shared<___AdNetworkModels___>())
,   m_appOpenAdManager(make_shared<___AppOpenAdManager___>())
{
    
}

___AdsHandler___::~___AdsHandler___()
{
    auto eventDispatcher = cocos2d::Director::getInstance()->getEventDispatcher();
    eventDispatcher->removeCustomEventListeners(ADS_LIMIT_SESSION_ENDED);
    ___unScheduleAdStuckEvent___();
}

void ___AdsHandler___::initializeAdsSDK(Layer* popupLayer)
{
    this->m_popupLayer = popupLayer;
    this->___addSearchPath___();
    this->___getAdsConfigFromParse___();
    this->___setupEasyNDK___();
    this->___initializeAdsSDK___();
    const float loadingLayerSpan = 60.0f;
    ___addLoadingLayerWithTimer___(loadingLayerSpan);

}

void ___AdsHandler___::___addSearchPath___()
{
    std::vector<std::string> searchPath = FileUtils::getInstance()->getSearchPaths();
    searchPath.push_back(("ModuleAdsResources"));
    FileUtils::getInstance()->setSearchPaths(searchPath);
}

void ___AdsHandler___::___setupEasyNDK___()
{
#if CC_TARGET_PLATFORM == CC_PLATFORM_IOS
    ___ModuleAdsBridge___::___initializeAdsHandler___();
#elif CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID
    CCLOG("AdsHandler::setupEasyNDK");
    ___CommonModuleUtils___::___setupEasyNDK___(("com/modules/ads/ModuleAds"), ("initialize"));
#endif
}

void ___AdsHandler___::___initializeAdsSDK___()
{
    cocos2d::ValueMap eventParams;
    sendMessageWithParams(("___initSDKs___"), cocos2d::Value(eventParams) , MODULE_ADS_NDK_MODULE_NAME);
}

void ___AdsHandler___::___preLoadAd___(___IAdListener___::___ADS_TYPE___ adType)
{
    ___tryPreLoadingAds___(adType);
}

void ___AdsHandler___::___tryPreLoadingAds___(___IAdListener___::___ADS_TYPE___ adType)
{
    const std::string& scheduleName = ___getAdTypeString___(adType);
    Director::getInstance()->getScheduler()->unschedule(scheduleName.c_str(), this);
    if(___CommonModuleUtils___::___isConnectedToNetwork___() && m_isAdsSDKFinishedInitilisation)
    {
        cocos2d::ValueMap eventParams;
        eventParams[("AdType")] = scheduleName.c_str();
        sendMessageWithParams(("___preLoadAds___"), cocos2d::Value(eventParams) , MODULE_ADS_NDK_MODULE_NAME);
    }
    else
    {
        const float retryInitializeDelay = 5.0f;
        Director::getInstance()->getScheduler()->schedule([this, adType](float delay)
        {
            ___tryPreLoadingAds___(adType);
        }, this, retryInitializeDelay, false, scheduleName.c_str());
    }
}

void ___AdsHandler___::___preLoadAllAds___()
{
//    ___preLoadAd___(___IAdListener___::___ADS_TYPE___::APPOPEN);
//    ___preLoadAd___(___IAdListener___::___ADS_TYPE___::INTERSTITIAL);
//    ___preLoadAd___(___IAdListener___::___ADS_TYPE___::VIDEO);
//    ___preLoadAd___(___IAdListener___::___ADS_TYPE___::BANNER);
}

void ___AdsHandler___::___getAdsConfigFromParse___()
{
    ___loadParseConfiguration___(("AdLimit"));
}

void ___AdsHandler___::___loadParseConfiguration___(const std::string& className)
{
    std::string filePath = ___CommonModuleUtils___::___getConfigsPath___() + className + (".plist");
    
    if (!FileUtils::getInstance()->isFileExist(filePath) || !___loadLocalConfigurations___(className, filePath))
    {
        filePath = className + (".plist");
        ___loadLocalConfigurations___(className, filePath);
    }
}

bool ___AdsHandler___::___loadLocalConfigurations___(const std::string& className, const std::string& filePath)
{
    if (className == ("AdLimit"))
    {
        return ___loadAdLimitConfiguration___(className, filePath);
    }
    return false;
}

bool ___AdsHandler___::___loadAdLimitConfiguration___(const std::string& key, const std::string& filePath)
{
    ValueMap valueMap = ___CommonModuleUtils___::___getValueMapFromFile___(filePath);
    if (!valueMap[("results")].isNull())
    {
        ValueVector results = valueMap[("results")].asValueVector();
        for (cocos2d::ValueVector::size_type i = 0 ; i < results.size(); i++)
        {
            ValueMap data = results[i].asValueMap();
            std::string adsLimitType = data[("Type")].asString();
            const int daysWait = data[("DaysWait")].asInt();
            const int limitSession = data[("LimitSession")].asInt();
            const int limitDay = data[("LimitDay")].asInt();
            
            ___AdsLimitModel___* model = new ___AdsLimitModel___();
            model->___setAdLimitType___(adsLimitType);
            model->___setDaysWait___(daysWait);
            model->___setLimitSession___(limitSession);
            model->___setLimitDay___(limitDay);
            
            m_adLimitModels[adsLimitType] = model;
        }
        return true;
    }
    return false;
}

void ___AdsHandler___::___forceAdFail___(___IAdListener___::___ADS_TYPE___ p_Type)
{
    ValueMap adStartedData = m_adStartedData.getType() == cocos2d::Value::Type::MAP ?
    m_adStartedData.asValueMap() : ValueMap();
    ValueMap valueMap;
    valueMap[("adType")] = (unsigned int)p_Type;
    valueMap[("failEvent")] = (unsigned int)___IAdListener___::___FAIL_SUBEVENTS___::PLAY;
    valueMap[("networkName")] = (adStartedData.find(("networkName")) != adStartedData.end()) ?
    adStartedData.at(("networkName")).asString() : ("Unknown");
    valueMap[("errorMessage")] = ("ForcedFail");
    ___adFailedCallback___(nullptr, cocos2d::Value(valueMap));
}

void ___AdsHandler___::___adFailedCallback___(Node *sender, cocos2d::Value data)
{
    ___unScheduleAdStuckEvent___();
    m_adFailedData = data;
    //Scheduler is necessary in order to fix UI Commpents turned into Black Box. MG-8301 & MG-8310
    Director::getInstance()->getScheduler()->schedule(schedule_selector(___AdsHandler___::___adFailedScheduledCallback___), this, 0, 0, 0, false);
}

void ___AdsHandler___::___adFailedScheduledCallback___(float dt)
{
    Director::getInstance()->getScheduler()->unschedule(schedule_selector(___AdsHandler___::___adFailedScheduledCallback___), this);
    ___removeLoadingLayer___();
    ___startSoundsAfterAd___();
    
    ValueMap& valueMap = m_adFailedData.asValueMap();
    ___IAdListener___::___ADS_TYPE___ adType = static_cast<___IAdListener___::___ADS_TYPE___>(valueMap[("adType")].asUnsignedInt());
    ___IAdListener___::___FAIL_SUBEVENTS___ eventType = static_cast<___IAdListener___::___FAIL_SUBEVENTS___>(valueMap[("failEvent")].asUnsignedInt());
    
    if (eventType == ___IAdListener___::___FAIL_SUBEVENTS___::PLAY)
    {
        std::string networkName = valueMap[("networkName")].asString();
        std::string errorMessage = valueMap[("errorMessage")].asString();
        std::string failCallbackLog = ("AdsHandler::adFailedCallback");
        failCallbackLog += ("::");
        failCallbackLog += networkName;
        failCallbackLog += ("::");
        failCallbackLog += ___getAdTypeString___(adType);
        failCallbackLog += ("::");
        failCallbackLog += errorMessage.c_str();
    }
    for_each_listener([this, adType, eventType](___IAdListener___* pListener)->void
    {
        pListener->___onAdFailed___(adType, eventType);
    });
}

void ___AdsHandler___::___adStartedCallback___(Node *sender, cocos2d::Value data)
{
    m_adStartedData = data;
    //Scheduler is necessary in order to fix UI Commpents turned into Black Box. MG-8301 & MG-8310
    Director::getInstance()->getScheduler()->schedule(schedule_selector(___AdsHandler___::___adStartedScheduledCallback___), this, 0, 0, 0, false);
}

std::string ___AdsHandler___::___getAdTypeString___(___IAdListener___::___ADS_TYPE___ adType)
{
    switch (adType)
    {
        case ___IAdListener___::___ADS_TYPE___::INTERSTITIAL:
            return ("Interstitial");
            break;
        case ___IAdListener___::___ADS_TYPE___::VIDEO:
            return ("Video");
            break;
        case ___IAdListener___::___ADS_TYPE___::BANNER:
            return ("Banner");
            break;
        case ___IAdListener___::___ADS_TYPE___::APPOPEN:
            return ("AppOpen");
            break;
    }
    return ("");
}

void ___AdsHandler___::___adStartedScheduledCallback___(float dt)
{
    Director::getInstance()->getScheduler()->unschedule(schedule_selector(___AdsHandler___::___adStartedScheduledCallback___), this);
    ValueMap& valueMap = m_adStartedData.asValueMap();
    ___IAdListener___::___ADS_TYPE___ adType = static_cast<___IAdListener___::___ADS_TYPE___>(valueMap[("adType")].asUnsignedInt());
    std::string networkName = valueMap[("networkName")].asString();
    std::string asTypeString = ___getAdTypeString___(adType);
    std::string startedCallbackLog = ("AdsHandler::adStartedCallback");
    startedCallbackLog += ("::");
    startedCallbackLog += networkName.c_str();
    startedCallbackLog += ("::");
    startedCallbackLog += asTypeString.c_str();
    for_each_listener([adType](___IAdListener___* pListener)
    {
        pListener->___onAdStarted___(adType);
    });
    
    if (m_loadingLayer && m_loadingLayer->getActionByTag(REMOVE_ACTION_TAG))
    {
        m_loadingLayer->stopAllActionsByTag(REMOVE_ACTION_TAG);
    }
}

void ___AdsHandler___::___adClosedCallback___(Node *sender, cocos2d::Value data)
{
    ___unScheduleAdStuckEvent___();
    m_adClosedData = data;
    Director::getInstance()->getScheduler()->schedule(schedule_selector(___AdsHandler___::___adClosedScheduledCallback___), this, 0, 0, 0, false);
}

void ___AdsHandler___::___adClosedScheduledCallback___(float dt)
{
    Director::getInstance()->getScheduler()->unschedule(schedule_selector(___AdsHandler___::___adClosedScheduledCallback___), this);
    ___removeLoadingLayer___();
    ___startSoundsAfterAd___();
    
    ValueMap& valueMap = m_adClosedData.asValueMap();
    ___IAdListener___::___ADS_TYPE___ adType = static_cast<___IAdListener___::___ADS_TYPE___>(valueMap[("adType")].asUnsignedInt());
    bool giveReward = valueMap[("giveReward")].asBool();
    std::string networkName = valueMap[("networkName")].asString();
    std::string closeCallbackLog = StringUtils::format(("AdsHandler::AdClosedCallback::%s"), networkName.c_str());
    const double adRevenue = (valueMap.find(("revenue")) != valueMap.end())
    ? valueMap[("revenue")].asDouble() : 0.0;
    std::string adTypeString = ___getAdTypeString___(adType);
    std::string adCompletionStatus = giveReward ? ("COMPLETED") : ("INCOMPLETE");
    std::string placementType;
    switch (adType)
    {
        case ___IAdListener___::___ADS_TYPE___::INTERSTITIAL:
            placementType = ("INTERSTITIAL");
            break;
        case ___IAdListener___::___ADS_TYPE___::VIDEO:
            placementType = ("REWARDED");
            break;
        case ___IAdListener___::___ADS_TYPE___::BANNER:
            placementType = ("BANNER");
            break;
        case ___IAdListener___::___ADS_TYPE___::APPOPEN:
            placementType = ("APPOPEN");
            break;
    }
    closeCallbackLog += ("::");
    closeCallbackLog += adTypeString.c_str();
    closeCallbackLog += ("::");
    closeCallbackLog += adCompletionStatus.c_str();

    m_lastAdRequester = ("");
    
    for_each_listener([this, adType, giveReward, closeCallbackLog](___IAdListener___* pListener)->void
    {
        switch (adType)
        {
            case ___IAdListener___::___ADS_TYPE___::INTERSTITIAL:
            case ___IAdListener___::___ADS_TYPE___::VIDEO:
            case ___IAdListener___::___ADS_TYPE___::APPOPEN:
            {
                if (adType == ___IAdListener___::___ADS_TYPE___::INTERSTITIAL)
                {
                    this->___updateLastInterstitialWatchedTime___(___CommonModuleUtils___::___getCurrentTimeInSeconds___());
                }
                else if (adType == ___IAdListener___::___ADS_TYPE___::VIDEO)
                {
                    this->___updateLastVideoWatchedTime___(___CommonModuleUtils___::___getCurrentTimeInSeconds___());
                }
                pListener->___onAdClosed___(adType, giveReward);
                break;
            }
            case ___IAdListener___::___ADS_TYPE___::BANNER:
                break;
        }
    });
}

void ___AdsHandler___::___showAdsFailPopUp___(const adsFailPopUpCloseCB closeCallback)
{
    if (closeCallback)
    {
        closeCallback();
    }
}

void ___AdsHandler___::___showInterstitialAd___()
{
    m_currAdTypeInProgress = ___IAdListener___::___ADS_TYPE___::INTERSTITIAL;
    const float loadingLayerSpan = 60.0f;
    this->___addLoadingLayerWithTimer___(loadingLayerSpan);

    if(___CommonModuleUtils___::___isConnectedToNetwork___())
    {
        if (m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::INTERSTITIAL))
        {
            const std::string& crashlyticsLog = StringUtils::format(("InterstitialAd is shown from %s network"), m_networkName.c_str());

            ValueMap valueMap;
            ___scheduleAdStuckEvent___();
            sendMessageWithParams(("___showInterstitialAd___"), cocos2d::Value(valueMap), MODULE_ADS_NDK_MODULE_NAME);
#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)
            bool isAds = true;
            cocos2d::Director::getInstance()->getEventDispatcher()->dispatchCustomEvent(MANAGED_BACKGROUND_TASK_STARTED, &isAds);
#endif
            return;
        }
    }
    ___forceAdFail___(m_currAdTypeInProgress);
}

void ___AdsHandler___::___showAppOpenAd___()
{
    m_currAdTypeInProgress = ___IAdListener___::___ADS_TYPE___::APPOPEN;
    const float loadingLayerSpan = 60.0f;
    this->___addLoadingLayerWithTimer___(loadingLayerSpan);

    if(___CommonModuleUtils___::___isConnectedToNetwork___())
    {
        if (m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::APPOPEN))
        {
            const std::string& crashlyticsLog = StringUtils::format(("AppOpenAd is shown from %s network"), m_networkName.c_str());

            ValueMap valueMap;
            ___scheduleAdStuckEvent___();
            sendMessageWithParams(("___showAppOpenAd___"), cocos2d::Value(valueMap), MODULE_ADS_NDK_MODULE_NAME);
#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)
            bool isAds = true;
            cocos2d::Director::getInstance()->getEventDispatcher()->dispatchCustomEvent(MANAGED_BACKGROUND_TASK_STARTED, &isAds);
#endif
            return;
        }
    }
    ___forceAdFail___(m_currAdTypeInProgress);
}

bool ___AdsHandler___::___isWatchAdAvailable___()
{
    const bool isRewardedAdFill = ___isRewardedAdFill___();
    const bool isRewardedVideoValidForDayLimit = ___isRewardedAdValidForDayLimit___();

    return isRewardedAdFill && isRewardedVideoValidForDayLimit;
}

void ___AdsHandler___::___showRewardedAd___(const std::string& adRequester)
{
    m_lastAdRequester = adRequester;
    m_currAdTypeInProgress = ___IAdListener___::___ADS_TYPE___::VIDEO;
    const float loadingLayerSpan = 60.0f;
    this->___addLoadingLayerWithTimer___(loadingLayerSpan);

    if(___CommonModuleUtils___::___isConnectedToNetwork___() && m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::VIDEO))
    {
        const std::string& crashlyticsLog = StringUtils::format(("VideoAd is shown from %s network"), m_networkName.c_str());

        ValueMap valueMap;
        ___scheduleAdStuckEvent___();
        sendMessageWithParams(("___showRewardedAd___"), cocos2d::Value(valueMap), MODULE_ADS_NDK_MODULE_NAME);
        m_adNetwork->___setAdCacheStatus___(___IAdListener___::___ADS_TYPE___::VIDEO, false);
#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)
        bool isAds = true;
        cocos2d::Director::getInstance()->getEventDispatcher()->dispatchCustomEvent(MANAGED_BACKGROUND_TASK_STARTED, &isAds);
#endif
        return;
    }
    ___forceAdFail___(m_currAdTypeInProgress);

}

void ___AdsHandler___::___sendGameAnalyticsWarning___(Node *sender, cocos2d::Value data) const
{
    std::string message = ("Force closing App at AdsHandler::sendGameAnalyticsWarning");
    EventCustom event(("CLOSE_APP"));
    event.setUserData(&message);
    cocos2d::Director::getInstance()->getEventDispatcher()->dispatchEvent(&event);
}

cocos2d::Size ___AdsHandler___::___getBannerSize___()
{
    if (m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::BANNER))
    {
        const cocos2d::Size& bannerSize = m_adNetwork->___getBannerSize___();
        if (bannerSize.width > 0 && bannerSize.height > 0)
        {
            return bannerSize;
        }
    }
    return cocos2d::Size::ZERO;
}

std::string ___AdsHandler___::___getCachedBannerNetwork___()
{
    //NOTE: shouldn't be displayed for paying user or if day to show not reached
    if (!this->___isBannerAdsValidForDayToShow___())
    {
        return ("");
    }
    
    if (m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::BANNER))
    {
        const cocos2d::Size& bannerSize = m_adNetwork->___getBannerSize___();
        if (bannerSize.width > 0 && bannerSize.height > 0)
        {
            return m_networkName.c_str();
        }
    }
    return ("");
}

cocos2d::Size ___AdsHandler___::___showBannerAd___()
{
    //NOTE: shouldn't be displayed for paying user or if day to show not reached
    if (!m_currentDisplayedBannerNetwork.empty())
    {
        return cocos2d::Size::ZERO;
    }

    if (m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::BANNER))
    {
        ValueMap valueMap;
        const cocos2d::Size& bannerSize = m_adNetwork->___getBannerSize___();
        if (bannerSize.width > 0 && bannerSize.height > 0)
        {
            m_currentDisplayedBannerNetwork = m_networkName.c_str();
            sendMessageWithParams(("___showBannerAd___"), cocos2d::Value(valueMap), MODULE_ADS_NDK_MODULE_NAME);
            return bannerSize;
        }
        else
        {
            ___postIncorrectBannerEvents___(m_networkName.c_str(), bannerSize.width, bannerSize.height);
        }
    }
    return cocos2d::Size::ZERO;
}

void ___AdsHandler___::___postIncorrectBannerEvents___(const std::string& adNetwork, const float width, const float height) const
{
    const std::string message = ___CommonModuleUtils___::___getStdStringWithFormat___(("Cached banner(%s) returned with incorrect size: %f x %f"), adNetwork.c_str(), width, height);
    ValueMap customErrorMap;
    customErrorMap[("message")] = message;
    customErrorMap[("domain")] = ("Ads Error");
    customErrorMap[("errorCode")] = ("0");
    // Post error on crashlytics
    // Post error on GameAnalytics
}

bool ___AdsHandler___::___hideBannerAd___()
{
    if (!m_currentDisplayedBannerNetwork.empty())
    {
        ValueMap valueMap;
        valueMap[("network")] = m_currentDisplayedBannerNetwork;
        sendMessageWithParams(("___hideBannerAd___"), cocos2d::Value(valueMap), MODULE_ADS_NDK_MODULE_NAME);
        m_currentDisplayedBannerNetwork = ("");
        return true;
    }

    return false;
}

void ___AdsHandler___::___reloadBanner___()
{
    ValueMap valueMap;
    sendMessageWithParams(("___reloadBannerAd___"), cocos2d::Value(valueMap), MODULE_ADS_NDK_MODULE_NAME);
}

const bool ___AdsHandler___::___isRewardedAdFill___() const
{
    return ___CommonModuleUtils___::___isConnectedToNetwork___() && m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::VIDEO);
}
const bool ___AdsHandler___::___isInterstitialAdFill___() const
{
    return ___CommonModuleUtils___::___isConnectedToNetwork___() && m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::INTERSTITIAL);
}

const bool ___AdsHandler___::___isBannerAdFill___() const
{
    return ___CommonModuleUtils___::___isConnectedToNetwork___() && m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::BANNER);
}

const bool ___AdsHandler___::___isAppOpenAdFill___() const
{
    return ___CommonModuleUtils___::___isConnectedToNetwork___() && m_adNetwork->___getAdCacheStatus___(___IAdListener___::___ADS_TYPE___::APPOPEN);
}

bool ___AdsHandler___::___shouldSkipInterstitialAd___()
{
    return !m_adsSkippingManager.___shouldShowInterstitialAd___();
}

bool ___AdsHandler___::___isBannerAdsValidForDayToShow___()
{
    ___AdsLimitModel___* limitModel = m_adLimitModels[BANNER_ADS_LIMIT_MODEL_KEY];
    const int daysToWait = limitModel->___getDaysWait___() * 24 * 60 * 60;
    time_t rawtime;
    time (&rawtime);
    const long curTime = rawtime;
    const long long gameInstallTime = ___CommonModule___::___getGameInstallTime___();
    const double timelapsed = curTime - gameInstallTime;
    
    return (timelapsed >= daysToWait);
}

void ___AdsHandler___::___recordRewardedAdForDayLimit___()
{
    //Update RewardedVideo Limit Status
    m_rewardedVideoCountInSession++;
    const std::string dateString = ___CommonModuleUtils___::___getCurrentDateString___();
    const std::string key = REWARDED_VIDEO_LOGGED_DATE_PREFIX+dateString;
    const int lastSavedLimit = UserDefault::getInstance()->getIntegerForKey(key.c_str(), 0) + 1;
    UserDefault::getInstance()->setIntegerForKey(key.c_str(), lastSavedLimit);
    UserDefault::getInstance()->flush();
}

void ___AdsHandler___::___recordPlacementAdsForDayLimit___()
{
    //Update RewardedVideo Limit Status
    m_placementAdsCountInSession++;
    const std::string dateString = ___CommonModuleUtils___::___getCurrentDateString___();
    const std::string key = PLACEMENT_ADS_LOGGED_DATE_PREFIX+dateString;
    const int lastSavedLimit = UserDefault::getInstance()->getIntegerForKey(key.c_str(), 0) + 1;
    UserDefault::getInstance()->setIntegerForKey(key.c_str(), lastSavedLimit);
    UserDefault::getInstance()->flush();
}

bool ___AdsHandler___::___isRewardedAdValidForDayLimit___()
{
    const std::string dateString = ___CommonModuleUtils___::___getCurrentDateString___();
    const std::string key = REWARDED_VIDEO_LOGGED_DATE_PREFIX + dateString;
    const int totalOffersInDay = UserDefault::getInstance()->getIntegerForKey(key.c_str(), 0);
    
    if (m_adLimitModels.find(REWARDED_VIDEO_LIMIT_MODEL_KEY) != m_adLimitModels.end())
    {
        ___AdsLimitModel___* limitModel = m_adLimitModels[REWARDED_VIDEO_LIMIT_MODEL_KEY];
        std::string allKeys = ("");
        for(std::map<std::string, ___AdsLimitModel___*>::iterator it = m_adLimitModels.begin(); it != m_adLimitModels.end(); ++it) {
            allKeys += it->first + (",");
        }
        const std::string& crashlyticsLog = StringUtils::format(("AdLimitModel size is %d allKeys:%s"), m_adLimitModels.size(), allKeys.c_str());

        if (m_rewardedVideoCountInSession < limitModel->___getLimitSession___() && totalOffersInDay < limitModel->___getLimitDay___())
        {
            return true;
        }
    }
    return false;
}

bool ___AdsHandler___::___isPlacementAdsValidForDayLimit___()
{
    if (m_adLimitModels.find(PLACEMENT_ADS_LIMIT_MODEL_KEY) != m_adLimitModels.end())
    {
        ___AdsLimitModel___* limitModel = m_adLimitModels[PLACEMENT_ADS_LIMIT_MODEL_KEY];
        const int daysToWait = limitModel->___getDaysWait___() * 24 * 60 * 60;
        time_t rawtime;
        time (&rawtime);
        long curTime = rawtime;
        
        const long long gameInstallTime = ___CommonModule___::___getGameInstallTime___();
        double timelapsed = curTime - gameInstallTime;
        
        const std::string dateString = ___CommonModuleUtils___::___getCurrentDateString___();
        const std::string key = PLACEMENT_ADS_LOGGED_DATE_PREFIX + dateString;
        const int totalOffersInDay = UserDefault::getInstance()->getIntegerForKey(key.c_str(), 0);

        if (m_placementAdsCountInSession < limitModel->___getLimitSession___() &&
            totalOffersInDay < limitModel->___getLimitDay___() &&
            timelapsed >= daysToWait)
        {
            return true;
        }
    }
    
    return false;    
}

bool ___AdsHandler___::___isAppOpenAdsValidForDayLimit___()
{
    if (m_adLimitModels.find(APP_OPEN_ADS_LIMIT_MODEL_KEY) != m_adLimitModels.end())
    {
        ___AdsLimitModel___* limitModel = m_adLimitModels[APP_OPEN_ADS_LIMIT_MODEL_KEY];
        const int daysToWait = limitModel->___getDaysWait___() * 24 * 60 * 60;
        time_t rawtime;
        time (&rawtime);
        long curTime = rawtime;
        
        const long long gameInstallTime = ___CommonModule___::___getGameInstallTime___();
        double timelapsed = curTime - gameInstallTime;
        
        const std::string dateString = ___CommonModuleUtils___::___getCurrentDateString___();
        const std::string key = APP_OPEN_ADS_LOGGED_DATE_PREFIX + dateString;
        const int totalOffersInDay = UserDefault::getInstance()->getIntegerForKey(key.c_str(), 0);

        if (m_placementAdsCountInSession < limitModel->___getLimitSession___() &&
            totalOffersInDay < limitModel->___getLimitDay___() &&
            timelapsed >= daysToWait)
        {
            return true;
        }
    }
    
    return false;
}

void ___AdsHandler___::___onAdsLimitSessionEndedEvent___()
{
    m_offersCountInSession = 0;
    m_rewardedVideoCountInSession = 0;
    m_placementAdsCountInSession = 0;
}

double ___AdsHandler___::___getPendingOffersReward___() const
{
    return UserDefault::getInstance()->getIntegerForKey(OFFERWALL_REWARD_USERDEFAULT_KEY, 0.0);
}

void ___AdsHandler___::___clearPendingOffersReward___()
{
    UserDefault::getInstance()->setIntegerForKey(OFFERWALL_REWARD_USERDEFAULT_KEY, 0.0);
    UserDefault::getInstance()->flush();
}

void ___AdsHandler___::___stopSoundsBeforeAd___()
{
//    ___SoundsHandler___::___pauseAll___();
}

void ___AdsHandler___::___startSoundsAfterAd___()
{
//    ___SoundsHandler___::___resumeAll___();
}

void ___AdsHandler___::___onAdsSDKInitializedCallback___(Node *sender, cocos2d::Value data)
{
    ___removeLoadingLayer___();
    m_isAdsSDKFinishedInitilisation = true;
}

void ___AdsHandler___::___setAdsCacheStatus___(Node *sender, cocos2d::Value data)
{
    ValueMap valueMap = data.asValueMap();
    const bool interstitialAdCache = valueMap[("AppLovinInterstitial")].asBool();
    const bool rewardedAdCache = valueMap[("AppLovinVideo")].asBool();
    const bool appOpenAdCache = valueMap[("AppLovinAppOpen")].asBool();
    ___updateAdCacheStatus___(___IAdListener___::___ADS_TYPE___::INTERSTITIAL, interstitialAdCache);
    ___updateAdCacheStatus___(___IAdListener___::___ADS_TYPE___::VIDEO, rewardedAdCache);
    ___updateAdCacheStatus___(___IAdListener___::___ADS_TYPE___::APPOPEN, appOpenAdCache);
    
    const auto bannerData = (valueMap.find(("AppLovinBanner")) != valueMap.end()) ?
    valueMap[("AppLovinBanner")].asValueMap() : cocos2d::ValueMap();
    ___updateBannerAdCacheStatus___(bannerData);
}

void ___AdsHandler___::___updateAdCacheStatus___(___IAdListener___::___ADS_TYPE___ pType, const bool newCache)
{
    if (m_adNetwork->___getAdCacheStatus___(pType) != newCache)
    {
        m_adNetwork->___setAdCacheStatus___(pType, newCache);
        for_each_listener([this, pType, newCache](___IAdListener___* pListener)->void
        {
            pListener->___onAdCacheStatusChanged___(pType, newCache);
        });
    }
}

void ___AdsHandler___::___updateBannerAdCacheStatus___(ValueMap bannerData)
{
    const bool newCache = (bannerData.find(("cached")) != bannerData.end()) ? bannerData[("cached")].asBool() : false;
    if (newCache)
    {
        const cocos2d::Size bannerSize(bannerData[("width")].asFloat(), bannerData[("height")].asFloat());
        m_adNetwork->___setBannerSize___(bannerSize);
    }
    ___updateAdCacheStatus___(___IAdListener___::___ADS_TYPE___::BANNER, newCache);
}

std::string ___AdsHandler___::___getNameForAdType___(___IAdListener___::___ADS_TYPE___ p_Type)
{
    switch(p_Type)
    {
        case ___IAdListener___::___ADS_TYPE___::VIDEO:
            return ("Video");
        case ___IAdListener___::___ADS_TYPE___::INTERSTITIAL:
            return ("Interstitial");
        case ___IAdListener___::___ADS_TYPE___::BANNER:
            return ("Banner");
        case ___IAdListener___::___ADS_TYPE___::APPOPEN:
            return ("AppOpen");
    }
}

void ___AdsHandler___::___scheduleAdStuckEvent___()
{
    const float delay = 60.0f;
    Director::getInstance()->getScheduler()->schedule([this](float dt)
    {
        ValueMap valueMap = m_adStartedData.getType() == cocos2d::Value::Type::MAP ?
        m_adStartedData.asValueMap() : ValueMap();
        std::string failCallbackLog = ("AdsHandler::adStuckTriggered");
        if (valueMap.find(("networkName")) != valueMap.end())
        {
            std::string networkName = valueMap[("networkName")].asString();
            failCallbackLog += ("::");
            failCallbackLog += networkName;
        }
        if (valueMap.find(("adType")) != valueMap.end())
        {
            ___IAdListener___::___ADS_TYPE___ adType =
            static_cast<___IAdListener___::___ADS_TYPE___>(valueMap[("adType")].asUnsignedInt());
            failCallbackLog += ("::");
            failCallbackLog += ___getAdTypeString___(adType);
        }
        if (valueMap.find(("errorMessage")) != valueMap.end())
        {
            std::string errorMessage = valueMap[("errorMessage")].asString();
            failCallbackLog += ("::");
            failCallbackLog += errorMessage.c_str();
        }
        ValueMap customErrorMap;
        customErrorMap[("message")] = failCallbackLog;
        customErrorMap[("domain")] = ("AD_STUCK");
        customErrorMap[("errorCode")] = ("0");
    }, this, delay, 0, 0, false, ("___scheduleAdStuckEvent___"));

}

void ___AdsHandler___::___unScheduleAdStuckEvent___()
{
    Director::getInstance()->getScheduler()->unschedule(("___scheduleAdStuckEvent___"), this);
}

void ___AdsHandler___::___addLoadingLayerWithTimer___(const float secondsToRemove)
{
    ___stopSoundsBeforeAd___();
    m_loadingLayer = ___CommonModuleUtils___::___getLoadingLayer___();
    m_loadingLayer->shouldBlockBackButton(true);
    m_popupLayer->addChild(m_loadingLayer);
//    ___ViewManager___::___getPopupLayer___()->addChild(m_loadingLayer);

    DelayTime* delayAction = DelayTime::create(secondsToRemove);
    CallFuncN* removeFunc = CallFuncN::create(CC_CALLBACK_1(___AdsHandler___::___removeLoadingLayer___, this));

    auto removeLoadingLayerAction = Sequence::create(delayAction, removeFunc, NULL);
    removeLoadingLayerAction->setTag(REMOVE_ACTION_TAG);
    m_loadingLayer->runAction(removeLoadingLayerAction);
}

void ___AdsHandler___::___removeLoadingLayer___(Node* pSender)
{
    if (m_loadingLayer)
    {
        m_loadingLayer->removeFromParentAndCleanup(true);
        m_loadingLayer = nullptr;

        if (pSender != nullptr)
        {
            ___forceAdFail___(m_currAdTypeInProgress);
        }
    }
}

void ___AdsHandler___::___registerListener___(___IAdListener___* pListener)
{
    this->addListener(pListener);
}

void ___AdsHandler___::___unregisterListener___(___IAdListener___* pListener)
{
    this->removeListener(pListener);
}

void ___AdsHandler___::___updateAdsCacheStatus___()
{
    sendMessageWithParams(("___updateAdsCacheStatus___"), cocos2d::Value() , MODULE_ADS_NDK_MODULE_NAME);
}

void ___AdsHandler___::___updateLastVideoWatchedTime___(const double time)
{
    m_adsSkippingManager.___updateLastVideoWatchedTime___(___CommonModuleUtils___::___getCurrentTimeInSeconds___());
}

void ___AdsHandler___::___updateLastVideoSkippedTime___(const double time)
{
    m_adsSkippingManager.___updateLastVideoSkippedTime___(___CommonModuleUtils___::___getCurrentTimeInSeconds___());
}

void ___AdsHandler___::___updateLastInterstitialWatchedTime___(const double time)
{
    m_adsSkippingManager.___updateLastInterstitialWatchedTime___(___CommonModuleUtils___::___getCurrentTimeInSeconds___());
}
