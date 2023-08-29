//
//  AdNetworkModels.cpp
//  ModuleAds
//
//  Created by Abdul Wasay on 19/08/2015.
//  Copyright (c) 2015 Gaminations. All rights reserved.
//

#include "AdNetworkModels.h"

___AdNetworkModels___::___AdNetworkModels___()
    :   m_platform(("NOT_SPECIFIED"))
    ,   m_interstitialAdCached(false)
    ,   m_rewardedAdCached(false)
    ,   m_bannerAdCached(false)
    ,   m_appOpenAdCached(false)
    ,   m_bannerSize(0.f, 0.f)
{

}

___AdNetworkModels___::~___AdNetworkModels___()
{

}

const bool ___AdNetworkModels___::___getAdCacheStatus___(const ___IAdListener___::___ADS_TYPE___ pAdType) const
{
    switch (pAdType)
    {
        case ___IAdListener___::___ADS_TYPE___::INTERSTITIAL :
        {
            return m_interstitialAdCached;
        }
            break;
        case ___IAdListener___::___ADS_TYPE___::VIDEO :
        {
            return m_rewardedAdCached;
        }
            break;
        case ___IAdListener___::___ADS_TYPE___::BANNER :
        {
            return m_bannerAdCached;
        }
            break;
        case ___IAdListener___::___ADS_TYPE___::APPOPEN :
        {
            return m_appOpenAdCached;
        }
            break;
        default:
            return false;
            break;
    }
}

void ___AdNetworkModels___::___setAdCacheStatus___(const ___IAdListener___::___ADS_TYPE___ pAdType,const bool isCached)
{
    switch (pAdType)
    {
        case ___IAdListener___::___ADS_TYPE___::INTERSTITIAL :
        {
            m_interstitialAdCached = isCached;
        }
            break;
        case ___IAdListener___::___ADS_TYPE___::VIDEO :
        {
            m_rewardedAdCached = isCached;
        }
            break;
        case ___IAdListener___::___ADS_TYPE___::BANNER :
        {
            m_bannerAdCached = isCached;
        }
            break;
        case ___IAdListener___::___ADS_TYPE___::APPOPEN :
        {
            m_appOpenAdCached = isCached;
        }
            break;

        default:
            break;
    }
}
