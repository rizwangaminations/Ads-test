//
//  AdsSkippingManager.cpp
//  ModuleAds
//
//  Created by Zeeshan Amjad on 02/07/2019.
//  Copyright © 2019 Gaminations. All rights reserved.
//

#include "AdsSkippingManager.h"

___AdsSkippingManager___::___AdsSkippingManager___()
: updateLastVideoWatchedTimeKey("updateLastVideoWatchedTimeKey")
, updateLastVideoSkippedTimeKey("updateLastVideoSkippedTimeKey")
, updateLastInterstitialWatchedTimeKey("updateLastInterstitialWatchedTimeKey")
, m_lastVideoWatchedTime(0)
, m_lastVideoSkippedTime(0)
, m_lastInterstitialWatchedTime(0)
{
}

void ___AdsSkippingManager___::___updateLastVideoWatchedTime___(const double time)
{
}

void ___AdsSkippingManager___::___updateLastVideoSkippedTime___(const double time)
{
}

void ___AdsSkippingManager___::___updateLastInterstitialWatchedTime___(const double time)
{
}

bool ___AdsSkippingManager___::___shouldShowInterstitialAd___() const
{
    
    return true;
}
