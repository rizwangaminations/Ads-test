//
//  AdsLimitModel.h
//  ModuleAds
//
//  Created by Zeeshan Amjad on 22/02/2016.
//  Copyright © 2016 Gaminations. All rights reserved.
//

#ifndef AdsLimitModel_h
#define AdsLimitModel_h

#include <stdio.h>
#include <iostream>

struct ___AdsLimitModel___
{
private:
    
    std::string  m_adLimitType; //Type of Ad to Limit (Placement Ads, Offer Wall, Rewarded Video)
    int          m_daysWait; //The number of days after the first session before ads are displayed in the game (relevant for Placement Ads only)
    int          m_limitSession; //The maximum number of ads displayed in one session.
    int          m_limitDay; //The maximum number of ads displayed in one day
    
public:
    
    const std::string& ___getAdLimitType___() const;
    void ___setAdLimitType___(const std::string& adLimitType);
    
    const int ___getDaysWait___() const;
    void ___setDaysWait___(const int daysWait);
    
    const int ___getLimitSession___() const;
    void ___setLimitSession___(int limitSession);
    
    const int ___getLimitDay___() const;
    void ___setLimitDay___(int limitDay);
    
};

#endif /* AdsLimitModel_h */
