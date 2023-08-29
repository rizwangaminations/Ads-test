//
//  AppOpenAdManager.h
//  ModuleAds
//
//  Created by Hassam Chaudhary on 19/01/2023.
//  Copyright © 2023 Gaminations. All rights reserved.
//

#ifndef AppOpenAdManager_h
#define AppOpenAdManager_h

#include "cocos2d.h"
#include "IAdListener.h"

using AdClosedCallback = std::function<void()>;
class ___AppOpenAdManager___ : public ___IAdListener___
{
private:
    bool                    m_showAppOpenAdWhenLoaded;
    bool                    m_showingAppOpenAd;
    AdClosedCallback        m_adClosedCallback;
    
    virtual void ___onAdStarted___(const ___ADS_TYPE___ pAdType) override;
    virtual void ___onAdClosed___(const ___ADS_TYPE___ pAdType, bool giveReward) override;
    virtual void ___onAdFailed___(const ___ADS_TYPE___ pAdType, const ___FAIL_SUBEVENTS___ p_Event) override;
    virtual void ___onAdCacheStatusChanged___(const ___ADS_TYPE___ pAdType, const bool isCashed) override;
    void ___tryToShowAppOpenAd___();
    void ___cancelAppOpenAd___();

    
public:
    ___AppOpenAdManager___();
    ~___AppOpenAdManager___();

    void ___showAppOpenAd___();
    void ___closeAppOpenAdWithCallback___(AdClosedCallback callback);
};


#endif /* AppOpenAdManager_h */
