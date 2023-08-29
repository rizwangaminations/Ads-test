/****************************************************************************
 Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.
 
 http://www.cocos2d-x.org
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
 ****************************************************************************/

#ifndef __HELLOWORLD_SCENE_H__
#define __HELLOWORLD_SCENE_H__

#include "cocos2d.h"

#include "../module-ads-include.h"

class HelloWorld : public cocos2d::Scene, public ___IAdListener___
{
public:


    static cocos2d::Scene* createScene();



private:
    HelloWorld();
    ~HelloWorld();
    static HelloWorld* create();

    virtual bool init();

    void menuCloseCallback(cocos2d::Ref* pSender);
    void showBannerAdCallback(cocos2d::Ref* pSender);
    void showInterAdCallback(cocos2d::Ref* pSender);
    void showVideoAdCallback(cocos2d::Ref* pSender);

    void loadBannerAdCallback(cocos2d::Ref* pSender);
    void loadInterAdCallback(cocos2d::Ref* pSender);
    void loadVideoAdCallback(cocos2d::Ref* pSender);

    void initializeAds();

    void addLogsText();
    void addBackButtonListener();
    void onKeyReleased(EventKeyboard::KeyCode keyCode, Event* event);

    void loadRewardedAd();
    void loadBannerAd();
    void loadInterAd();

    void showRewardedAd();
    void showBannerAd();
    void showInterAd();

    virtual void ___onAdStarted___(const ___ADS_TYPE___ pAdType) override;
    virtual void ___onAdClosed___(const ___ADS_TYPE___ pAdType, bool giveReward) override;
    virtual void ___onAdFailed___(const ___ADS_TYPE___ pAdType, const ___FAIL_SUBEVENTS___ p_Event) override;
    virtual void ___onAdCacheStatusChanged___(const ___ADS_TYPE___ pAdType, const bool isCashed) override;

private:
    MenuItemImage*                m_showBannerAdItem;
    MenuItemImage*                m_showInterAdItem;
    MenuItemImage*                m_showVideoAdItem;

    MenuItemImage*                m_loadBannerAdItem;
    MenuItemImage*                m_loadInterAdItem;
    MenuItemImage*                m_loadVideoAdItem;

    bool                          m_bannerAdVisible;

    EventListenerKeyboard*        m_keyBoardListner;

    Label*                        m_backbuttonLog;
    Label*                        m_bannerAdLogs;
    Label*                        m_interAdLogs;
    Label*                        m_videoAdLogs;

    int                           m_backCount;
};

#endif // __HELLOWORLD_SCENE_H__
