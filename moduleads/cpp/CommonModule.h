//
//  CommonModule.h
//  ModuleCommon
//
//  Created by Muhammad Arslan on 15/08/2015.
//  Copyright (c) 2015 Gaminations. All rights reserved.
//

#ifndef CommonModule_h__
#define CommonModule_h__

#include "CommonModuleConstants.h"
#include "cocos2d.h"

using namespace cocos2d;

class ___CommonModule___
{
private:
    long long m_gameInstallTimeStamp;
    EventListenerCustom* m_releaseCachedResourcesObserver;
    static ___CommonModule___* m_instance;
    std::vector<Texture2D*> m_retainedTextures;
    std::vector<SpriteFrame*> m_retainedSpriteFrames;
    bool m_didReceiveMemoryWarning;
    std::vector<std::string> m_mainMenuResources;
    std::vector<std::string> m_levelResources;
    bool m_isInternetConnected;
    std::string m_currencyCode;
    std::string m_gameSettingsConfigName;

private:
    ___CommonModule___();
    virtual ~___CommonModule___();

    static ___CommonModule___* getInstance();
    static void ___destroyInstance___();
    virtual bool init();

    static void ___addSearchPath___();
    static void ___setupEasyNDK___();

public:
    static void ___initialize___();

    static long long ___getGameInstallTime___();
    static int ___getDaysPassedFromInstallation___();

    static inline bool ___getDidReceiveMemoryWarning___() { return ___CommonModule___::getInstance()->m_didReceiveMemoryWarning; }
    static inline void ___setDidReceiveMemoryWarning___(bool memoryWarningValue) {
        ___CommonModule___::getInstance()->m_didReceiveMemoryWarning = memoryWarningValue;
    }
    static inline bool ___isEnableAds___()
    {
        return true;
    }
    
#if CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID
    static inline bool ___getIsInternetConnected___() { return ___CommonModule___::getInstance()->m_isInternetConnected; }
#endif
    void ___onInternetConnectivityChange___(Node *sender, cocos2d::Value data);
};

#endif // CommonModule_h__
