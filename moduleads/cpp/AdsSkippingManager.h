//
//  AdsSkippingManager.h
//  ModuleAds
//
//  Created by Zeeshan Amjad on 02/07/2019.
//  Copyright © 2019 Gaminations. All rights reserved.
//

#ifndef AdsSkippingManager_h
#define AdsSkippingManager_h

#include <stdio.h>
#include <string>

class ___AdsSkippingManager___ {
private:
    double m_lastVideoWatchedTime;
    double m_lastVideoSkippedTime;
    double m_lastInterstitialWatchedTime;
    
    const std::string updateLastVideoWatchedTimeKey;
    const std::string updateLastVideoSkippedTimeKey;
    const std::string updateLastInterstitialWatchedTimeKey;
    
public:
    ___AdsSkippingManager___();
    
    void ___updateLastVideoWatchedTime___(const double time);
    void ___updateLastVideoSkippedTime___(const double time);
    void ___updateLastInterstitialWatchedTime___(const double time);
    
    bool ___shouldShowInterstitialAd___() const;
    
};

#endif /* AdsSkippingManager_h */
