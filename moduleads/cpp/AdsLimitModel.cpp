//
//  AdsLimitModel.cpp
//  ModuleAds
//
//  Created by Zeeshan Amjad on 22/02/2016.
//  Copyright © 2016 Gaminations. All rights reserved.
//

#include "AdsLimitModel.h"

const std::string& ___AdsLimitModel___::___getAdLimitType___() const
{
    return m_adLimitType;
}

void ___AdsLimitModel___::___setAdLimitType___(const std::string& adLimitType)
{
    m_adLimitType = adLimitType;
}

const int ___AdsLimitModel___::___getDaysWait___() const
{
    return m_daysWait;
}

void ___AdsLimitModel___::___setDaysWait___(const int daysWait)
{
    m_daysWait = daysWait;
}

const int ___AdsLimitModel___::___getLimitSession___() const
{
    return m_limitSession;
}

void ___AdsLimitModel___::___setLimitSession___(int limitSession)
{
    m_limitSession = limitSession;
}

const int ___AdsLimitModel___::___getLimitDay___() const
{
    return m_limitDay;
}

void ___AdsLimitModel___::___setLimitDay___(int limitDay)
{
    m_limitDay = limitDay;
}
