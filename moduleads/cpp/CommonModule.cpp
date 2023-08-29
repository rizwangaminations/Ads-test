//
//  CommonModule.cpp
//  ModuleCommon
//
//  Created by Muhammad Arslan on 15/08/2015.
//  Copyright (c) 2015 Gaminations. All rights reserved.
//

#include "CommonModule.h"
#include "CommonModuleUtils.h"
#include "FairyGUI.h"
#include "ThirdParty/NDKHelper/NDKHelper/NDKHelper.h"

USING_NS_FGUI;

using namespace std;

___CommonModule___* ___CommonModule___::m_instance = nullptr;

___CommonModule___::___CommonModule___()
    : m_releaseCachedResourcesObserver(nullptr)
    , m_didReceiveMemoryWarning(false)
    , m_isInternetConnected(true)
    , m_currencyCode(("USD"))
    , m_gameSettingsConfigName("")
{
}

___CommonModule___::~___CommonModule___()
{
    if(m_releaseCachedResourcesObserver)
    {
        auto eventDispatcher = cocos2d::Director::getInstance()->getEventDispatcher();
        eventDispatcher->removeEventListener(m_releaseCachedResourcesObserver);
    }
}

___CommonModule___* ___CommonModule___::getInstance()
{
    if (!m_instance)
    {
        m_instance = new ___CommonModule___();
        CCASSERT(m_instance, "FATAL: Not enough memory");
        m_instance->init();
    }

    return m_instance;
}

void ___CommonModule___::___destroyInstance___()
{
    delete m_instance;
    m_instance = nullptr;
}

bool ___CommonModule___::init()
{
    NDKHelper::addSelector(("ndk-receiver-common-module"), ("onInternetConnectivityChange"), CC_CALLBACK_2(___CommonModule___::___onInternetConnectivityChange___, this), nullptr);
    return true;
}

void ___CommonModule___::___initialize___()
{
    ___CommonModule___::___addSearchPath___();
    ___CommonModule___ *instance = ___CommonModule___::getInstance();
    ___CommonModule___::___setupEasyNDK___();
}

void ___CommonModule___::___onInternetConnectivityChange___(Node *sender, cocos2d::Value data)
{
    ValueMap dataMap = data.asValueMap();
    m_isInternetConnected = dataMap[("isInternetConnected")].asBool();
}

void ___CommonModule___::___setupEasyNDK___()
{
    ___CommonModuleUtils___::___setupEasyNDK___(("com/modules/common/ModuleCommon"), ("initialize"));
}

void ___CommonModule___::___addSearchPath___()
{
}


/*static*/ long long ___CommonModule___::___getGameInstallTime___()
{
    return ___CommonModule___::getInstance()->m_gameInstallTimeStamp;
}



int ___CommonModule___::___getDaysPassedFromInstallation___()
{
    const double gameInstallTime = static_cast<double>(___CommonModule___::___getGameInstallTime___());
    const double now = static_cast<double>(___CommonModuleUtils___::___getCurrentTimeInSeconds___());
    const double nDaysGone = (now - gameInstallTime) / (24.0 * 60.0 * 60.0);

    return static_cast<int>(nDaysGone);
}
