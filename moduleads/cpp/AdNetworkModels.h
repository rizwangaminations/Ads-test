//
//  AdNetworkModels.h
//  ModuleAds
//
//  Created by Abdul Wasay on 19/08/2015.
//  Copyright (c) 2015 Gaminations. All rights reserved.
//

#ifndef __ModuleAds__AdNetworkModels__
#define __ModuleAds__AdNetworkModels__

#include <stdio.h>
#include "cocos2d.h"
#include "IAdListener.h"


using namespace cocos2d;
struct ___AdNetworkModels___
{
public:
    ___AdNetworkModels___();
    ~___AdNetworkModels___();

    inline const std::string& ___getPlatform___() const { return m_platform; }
    inline void ___setPlatform___(const std::string& platform) { m_platform = platform; }
    const bool ___getAdCacheStatus___(const ___IAdListener___::___ADS_TYPE___ pAdType) const;
    void ___setAdCacheStatus___(const ___IAdListener___::___ADS_TYPE___ pAdType,const bool isCached);
    inline const cocos2d::Size& ___getBannerSize___() const { return m_bannerSize; }
    inline void ___setBannerSize___(const cocos2d::Size& bannerSize) { m_bannerSize = bannerSize; }
    
private:
    std::string   m_platform;
    bool          m_interstitialAdCached;
    bool          m_rewardedAdCached;
    bool          m_bannerAdCached;
    bool          m_appOpenAdCached;
    cocos2d::Size m_bannerSize;
};

#endif /* defined(__ModuleAds__AdNetworkModels__) */
