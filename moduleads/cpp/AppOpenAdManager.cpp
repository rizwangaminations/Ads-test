//
//  AppOpenAdManager.cpp
//  ModuleAds
//
//  Created by Hassam Chaudhary on 19/01/2023.
//  Copyright © 2023 Gaminations. All rights reserved.
//

#include "AppOpenAdManager.h"
#include "AdsHandler.h"

___AppOpenAdManager___::___AppOpenAdManager___()
: m_showAppOpenAdWhenLoaded(false)
, m_showingAppOpenAd(false)
, m_adClosedCallback(nullptr)
{
}

___AppOpenAdManager___::~___AppOpenAdManager___()
{
}

/*virtual*/ void ___AppOpenAdManager___::___onAdStarted___(const ___ADS_TYPE___ pAdType) /*override*/
{
    switch (pAdType)
    {
        case ___ADS_TYPE___::APPOPEN:
        {
            m_showingAppOpenAd = true;
        }
            break;
        case ___ADS_TYPE___::VIDEO:
        case ___IAdListener___::___ADS_TYPE___::INTERSTITIAL:
        case ___IAdListener___::___ADS_TYPE___::BANNER:
            break;
    }
}

/*virtual*/ void ___AppOpenAdManager___::___onAdClosed___(const ___ADS_TYPE___ pAdType, bool giveReward) /*override*/
{
    switch (pAdType)
    {
        case ___ADS_TYPE___::APPOPEN:
        {
            ___cancelAppOpenAd___();
        }
            break;
        case ___ADS_TYPE___::VIDEO:
        case ___IAdListener___::___ADS_TYPE___::INTERSTITIAL:
        case ___IAdListener___::___ADS_TYPE___::BANNER:
            break;
    }
}

/*virtual*/ void ___AppOpenAdManager___::___onAdFailed___(const ___ADS_TYPE___ pAdType, const ___FAIL_SUBEVENTS___ p_Event) /*override*/
{
    ___cancelAppOpenAd___();
}

/*virtual*/ void ___AppOpenAdManager___::___onAdCacheStatusChanged___(const ___ADS_TYPE___ pAdType, const bool isCashed) /*override*/
{
    switch(pAdType)
    {
        case ___ADS_TYPE___::APPOPEN:
        {
            if (isCashed && m_showAppOpenAdWhenLoaded)
            {
                ___tryToShowAppOpenAd___();
            }
        }
            break;
        case ___ADS_TYPE___::VIDEO:
        case ___ADS_TYPE___::INTERSTITIAL:
        case ___ADS_TYPE___::BANNER:
            break;
    }
}

void ___AppOpenAdManager___::___showAppOpenAd___()
{
    ___AdsHandler___::___getInstance___()->___registerListener___(this);
    ___tryToShowAppOpenAd___();
}

void ___AppOpenAdManager___::___tryToShowAppOpenAd___()
{
    m_showAppOpenAdWhenLoaded = true;
    const bool isAppOpenAdCached = ___AdsHandler___::___getInstance___()->___isAppOpenAdFill___();
    if (isAppOpenAdCached)
    {
        m_showAppOpenAdWhenLoaded = false;
        ___AdsHandler___::___getInstance___()->___showAppOpenAd___();
    }
}

void ___AppOpenAdManager___::___cancelAppOpenAd___()
{
    ___AdsHandler___::___getInstance___()->___unregisterListener___(this);
    m_showAppOpenAdWhenLoaded = false;
    m_showingAppOpenAd = false;
    if (m_adClosedCallback)
    {
        m_adClosedCallback();
        m_adClosedCallback = nullptr;
    }
}

void ___AppOpenAdManager___::___closeAppOpenAdWithCallback___(AdClosedCallback callback)
{
    m_adClosedCallback = callback;
    if (!m_showingAppOpenAd)
    {
        ___cancelAppOpenAd___();
    }
}
