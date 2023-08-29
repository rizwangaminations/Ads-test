//
//  AdsHandler.h
//  ModuleAds
//
//  Created by Abdul Wasay on 17/08/2015.
//  Copyright (c) 2015 Gaminations. All rights reserved.
//

#ifndef __ModuleAds__AdsHandler__
#define __ModuleAds__AdsHandler__

#include "cocos2d.h"
#include "AdNetworkModels.h"
#include "AdsLimitModel.h"
#include "ModuleAdsConstants.h"
#include "CommonModuleUtils.h"
#include "IListening.h"
#include "IAdListener.h"
#include "AdsSkippingManager.h"

using namespace cocos2d;
using namespace std;

class ___AppOpenAdManager___;
class ___AdsHandler___ : public Ref, private IListening<___IAdListener___>
{
private:
    typedef std::function<void(void)> adsFailPopUpCloseCB;
    void ___initializeAdsSDK___();
    void ___tryPreLoadingAds___(___IAdListener___::___ADS_TYPE___ adType);

public:
    static ___AdsHandler___* ___getInstance___();
    void initializeAdsSDK(Layer* popupLayer);
    
    void ___preLoadAd___(___IAdListener___::___ADS_TYPE___ adType);
    void ___preLoadAllAds___();
    
    void ___showInterstitialAd___();
    void ___showAppOpenAd___();
    
    void ___showRewardedAd___(const std::string& adRequester);
    
    cocos2d::Size ___getBannerSize___();
    std::string ___getCachedBannerNetwork___();
    cocos2d::Size ___showBannerAd___();
    bool ___hideBannerAd___();
    void ___reloadBanner___();

    const bool ___isRewardedAdFill___() const;
    const bool ___isInterstitialAdFill___() const;
    const bool ___isAppOpenAdFill___() const;
    const bool ___isBannerAdFill___() const;

    bool ___shouldSkipInterstitialAd___();
    bool ___isRewardedAdValidForDayLimit___();
    bool ___isPlacementAdsValidForDayLimit___();
    bool ___isAppOpenAdsValidForDayLimit___();

    void ___showAdsFailPopUp___(const adsFailPopUpCloseCB closeCallback);
    void ___recordRewardedAdForDayLimit___();
    void ___recordPlacementAdsForDayLimit___();
    void ___registerListener___(___IAdListener___* pListener);
    void ___unregisterListener___(___IAdListener___* pListener);

    double ___getPendingOffersReward___() const;
    void ___clearPendingOffersReward___();

    void ___updateAdsCacheStatus___();

    void ___updateLastVideoWatchedTime___(const double time);
    void ___updateLastVideoSkippedTime___(const double time);
    void ___updateLastInterstitialWatchedTime___(const double time);
    bool ___isWatchAdAvailable___();
    
    inline shared_ptr<___AppOpenAdManager___> ___getAppOpenAdManager___() { return m_appOpenAdManager; }
private:

    ___AdsHandler___();
    virtual ~___AdsHandler___();

    std::string ___getNameForAdType___(___IAdListener___::___ADS_TYPE___ p_Type);

    void ___destroyInstance___();
    void ___addSearchPath___();
    void ___setupEasyNDK___();

    virtual bool ___init___();

    void ___getAdsConfigFromParse___();
    void ___setAdsCacheStatus___(Node *sender, cocos2d::Value data);
    void ___updateAdCacheStatus___(___IAdListener___::___ADS_TYPE___ pType, const bool newCache);
    void ___updateBannerAdCacheStatus___(ValueMap valueMap);

    void ___forceAdFail___(___IAdListener___::___ADS_TYPE___ p_Type);
    void ___onAdsSDKInitializedCallback___(Node *sender, cocos2d::Value data);
    void ___adClosedCallback___(Node *sender, cocos2d::Value data);
    void ___adStartedCallback___(Node *sender, cocos2d::Value data);
    void ___adFailedCallback___(Node *sender, cocos2d::Value data);
    
    void ___sendGameAnalyticsWarning___(Node *sender, cocos2d::Value data) const;

    void ___adFailedScheduledCallback___(float dt);
    void ___adClosedScheduledCallback___(float dt);
    void ___adStartedScheduledCallback___(float dt);

    void ___loadParseConfiguration___(const std::string& className);
    bool ___loadAdLimitConfiguration___(const std::string& key, const std::string& filePath);
    bool ___loadLocalConfigurations___(const std::string& key, const std::string& filePath);

    void ___stopSoundsBeforeAd___();
    void ___startSoundsAfterAd___();

    bool ___isBannerAdsValidForDayToShow___();
    void ___onAdsLimitSessionEndedEvent___();

    void ___scheduleAdStuckEvent___();
    void ___unScheduleAdStuckEvent___();
    void ___addLoadingLayerWithTimer___(const float secondsToRemove);
    void ___removeLoadingLayer___(Node* pSender = nullptr);

    void ___postIncorrectBannerEvents___(const std::string& adNetwork, const float width, const float height) const;
#pragma mark parseCallbacks

private:
    bool m_isParsingDone;
    bool m_isAdsSDKFinishedInitilisation;

    ___IAdListener___::___ADS_TYPE___  m_currAdTypeInProgress;
    shared_ptr<___AdNetworkModels___>  m_adNetwork;
    shared_ptr<___AppOpenAdManager___> m_appOpenAdManager;
    std::string m_currentDisplayedBannerNetwork;

    std::map<std::string, ___AdsLimitModel___*> m_adLimitModels;

    int m_offersCountInSession;
    int m_rewardedVideoCountInSession;
    int m_placementAdsCountInSession;
    
    cocos2d::Value m_adClosedData;
    cocos2d::Value m_adStartedData;
    cocos2d::Value m_adFailedData;

    Layer* m_popupLayer;
    ___CommonLoadingLayer___* m_loadingLayer;
    ___AdsSkippingManager___ m_adsSkippingManager;
    std::string m_lastAdRequester;
    const std::string m_networkName;
    std::string ___getAdTypeString___(___IAdListener___::___ADS_TYPE___ adType);
    
};
#endif //__ModuleAds__AdsHandler__
