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

#include "HelloWorldScene.h"
#include "SimpleAudioEngine.h"
#include "FairyGUI.h"

USING_NS_CC;
USING_NS_FGUI;

Scene* HelloWorld::createScene()
{
    return HelloWorld::create();
}

/*static*/ HelloWorld* HelloWorld::create()
{
    HelloWorld *pRet = new(std::nothrow) HelloWorld();
    if (pRet && pRet->init())
    {
        pRet->autorelease();
        return pRet;
    }
    else
    {
        delete pRet;
        pRet = nullptr;
        return nullptr;
    }
}

HelloWorld::HelloWorld()
: m_showBannerAdItem(nullptr)
, m_showInterAdItem(nullptr)
, m_showVideoAdItem(nullptr)
, m_loadBannerAdItem(nullptr)
, m_loadInterAdItem(nullptr)
, m_loadVideoAdItem(nullptr)
, m_keyBoardListner(nullptr)
, m_backbuttonLog(nullptr)
, m_bannerAdLogs(nullptr)
, m_interAdLogs(nullptr)
, m_videoAdLogs(nullptr)
, m_backCount(0)
, m_bannerAdVisible(false)
{

}

HelloWorld::~HelloWorld()
{
    _eventDispatcher->removeEventListener(m_keyBoardListner);
    ___AdsHandler___::___getInstance___()->___unregisterListener___(this);
}

bool HelloWorld::init()
{
    if ( !Scene::init() )
    {
        return false;
    }

    auto visibleSize = Director::getInstance()->getVisibleSize();
    Vec2 origin = Director::getInstance()->getVisibleOrigin();


    m_loadBannerAdItem = MenuItemImage::create(
            "loadBanner.png",
            "loadBanner.png",
            CC_CALLBACK_1(HelloWorld::loadBannerAdCallback, this));

    m_loadBannerAdItem->setPosition(Vec2(30,600));
    m_loadBannerAdItem->setAnchorPoint(Vec2::ANCHOR_MIDDLE_LEFT);

    m_loadInterAdItem = MenuItemImage::create(
            "loadInter.png",
            "loadInter.png",
            CC_CALLBACK_1(HelloWorld::loadInterAdCallback, this));

    m_loadInterAdItem->setPosition(Vec2(30,500));
    m_loadInterAdItem->setAnchorPoint(Vec2::ANCHOR_MIDDLE_LEFT);

    m_loadVideoAdItem = MenuItemImage::create(
            "loadRewarded.png",
            "loadRewarded.png",
            CC_CALLBACK_1(HelloWorld::loadVideoAdCallback, this));

    m_loadVideoAdItem->setPosition(Vec2(30,400));
    m_loadVideoAdItem->setAnchorPoint(Vec2::ANCHOR_MIDDLE_LEFT);


    /////

    m_showBannerAdItem = MenuItemImage::create(
            "showBanner.png",
            "showBanner.png",
            CC_CALLBACK_1(HelloWorld::showBannerAdCallback, this));

    m_showBannerAdItem->setPosition(Vec2(visibleSize.width - 30,600));
    m_showBannerAdItem->setVisible(false);
    m_showBannerAdItem->setAnchorPoint(Vec2::ANCHOR_MIDDLE_RIGHT);

    m_showInterAdItem = MenuItemImage::create(
            "showInter.png",
            "showInter.png",
            CC_CALLBACK_1(HelloWorld::showInterAdCallback, this));

    m_showInterAdItem->setPosition(Vec2(visibleSize.width - 30,500));
    m_showInterAdItem->setVisible(false);
    m_showInterAdItem->setAnchorPoint(Vec2::ANCHOR_MIDDLE_RIGHT);

    m_showVideoAdItem = MenuItemImage::create(
            "showRewarded.png",
            "showRewarded.png",
            CC_CALLBACK_1(HelloWorld::showVideoAdCallback, this));

    m_showVideoAdItem->setPosition(Vec2(visibleSize.width - 30,400));
    m_showVideoAdItem->setVisible(false);
    m_showVideoAdItem->setAnchorPoint(Vec2::ANCHOR_MIDDLE_RIGHT);

    auto closeItem = MenuItemImage::create(
                                           "CloseNormal.png",
                                           "CloseSelected.png",
                                           CC_CALLBACK_1(HelloWorld::menuCloseCallback, this));

    closeItem->setPosition(Vec2(visibleSize.width - 100,100));
    closeItem->setScale(3);


    auto menu = Menu::create(closeItem, m_showInterAdItem, m_showVideoAdItem, m_showBannerAdItem,
                             m_loadBannerAdItem, m_loadInterAdItem, m_loadVideoAdItem, NULL);
    menu->setPosition(Vec2::ZERO);
    this->addChild(menu, 1);

    auto sprite = Sprite::create("HelloWorld.png");
    sprite->setPosition(Vec2(visibleSize.width/2 + origin.x, visibleSize.height/2 + 200));
    this->addChild(sprite, 0);


    addLogsText();
    addBackButtonListener();
    initializeAds();
    return true;
}

void HelloWorld::addLogsText()
{
    std::string buttonText = StringUtils::format("back button pressed for %i times", m_backCount);
    m_backbuttonLog = Label::createWithTTF(buttonText.c_str(), "fonts/Marker Felt.ttf", 44);
    m_backbuttonLog->setPosition(Vec2(20,140));

    m_backbuttonLog->setAnchorPoint(Vec2::ANCHOR_MIDDLE_LEFT);
    this->addChild(m_backbuttonLog, 1);

    m_bannerAdLogs = Label::createWithTTF("Banner Ad loaded = false", "fonts/Marker Felt.ttf", 44);
    m_bannerAdLogs->setPosition(Vec2(20,200));

    m_bannerAdLogs->setAnchorPoint(Vec2::ANCHOR_MIDDLE_LEFT);
    this->addChild(m_bannerAdLogs, 1);

    ////
    m_interAdLogs = Label::createWithTTF("Inter Ad loaded = false", "fonts/Marker Felt.ttf", 44);
    m_interAdLogs->setPosition(Vec2(20,260));

    m_interAdLogs->setAnchorPoint(Vec2::ANCHOR_MIDDLE_LEFT);
    this->addChild(m_interAdLogs, 1);

    ////
    m_videoAdLogs = Label::createWithTTF("Video Ad loaded = false", "fonts/Marker Felt.ttf", 44);
    m_videoAdLogs->setPosition(Vec2(20,320));

    m_videoAdLogs->setAnchorPoint(Vec2::ANCHOR_MIDDLE_LEFT);
    this->addChild(m_videoAdLogs, 1);
}

void HelloWorld::initializeAds()
{
    Layer* popupLayer = Layer::create();
    popupLayer->setName("PopupLayer");
    addChild(popupLayer,2);

    ___AdsHandler___::___getInstance___()->initializeAdsSDK(popupLayer);
    ___AdsHandler___::___getInstance___()->___registerListener___(this);
}

void HelloWorld::menuCloseCallback(Ref* pSender)
{
    Director::getInstance()->end();
}

void HelloWorld::showBannerAdCallback(cocos2d::Ref* pSender)
{
    if (___AdsHandler___::___getInstance___()->___isBannerAdFill___())
    {
        showBannerAd();
    }
}

void HelloWorld::loadBannerAdCallback(cocos2d::Ref* pSender)
{
    m_loadBannerAdItem->setVisible(false);
    ___AdsHandler___::___getInstance___()->___preLoadAd___(___ADS_TYPE___::BANNER);
}

void HelloWorld::loadInterAdCallback(cocos2d::Ref* pSender)
{
    m_loadInterAdItem->setVisible(false);
    ___AdsHandler___::___getInstance___()->___preLoadAd___(___ADS_TYPE___::INTERSTITIAL);
}

void HelloWorld::loadVideoAdCallback(cocos2d::Ref* pSender)
{
    m_loadVideoAdItem->setVisible(false);
    ___AdsHandler___::___getInstance___()->___preLoadAd___(___ADS_TYPE___::VIDEO);
}

void HelloWorld::showInterAdCallback(cocos2d::Ref* pSender)
{
    if (___AdsHandler___::___getInstance___()->___isInterstitialAdFill___())
    {
        showInterAd();
    }
}

void HelloWorld::showVideoAdCallback(cocos2d::Ref* pSender)
{
    if (___AdsHandler___::___getInstance___()->___isRewardedAdFill___())
    {
        showRewardedAd();
    }
}

void HelloWorld::showRewardedAd()
{
    ___AdsHandler___::___getInstance___()->___showRewardedAd___("testAds");
}

void HelloWorld::showBannerAd()
{
    if (m_bannerAdVisible)
    {
        m_bannerAdVisible = false;
        ___AdsHandler___::___getInstance___()->___hideBannerAd___();
        m_bannerAdLogs->setString("banner ad hidden");
    }
    else
    {
        m_bannerAdVisible = true;
        ___AdsHandler___::___getInstance___()->___showBannerAd___();
        m_bannerAdLogs->setString("banner ad visible");
    }

}

void HelloWorld::showInterAd()
{
    ___AdsHandler___::___getInstance___()->___showInterstitialAd___();
}

/*virtual*/void HelloWorld::___onAdStarted___(const ___ADS_TYPE___ pAdType)
{
    switch (pAdType)
    {
        case ___ADS_TYPE___::VIDEO:
        {
            m_videoAdLogs->setString("Rewarded ad Started");
        }
            break;
        case ___ADS_TYPE___::BANNER:
            break;
        case ___ADS_TYPE___::INTERSTITIAL:
        {
            m_interAdLogs->setString("Inter ad Started");
        }
            break;
        case ___ADS_TYPE___::APPOPEN:
            break;
    }
}

/*virtual*/void HelloWorld::___onAdClosed___(const ___ADS_TYPE___ pAdType, bool giveReward)
{
    switch (pAdType)
    {
        case ___ADS_TYPE___::VIDEO: {
            m_videoAdLogs->setString("Rewarded ad Closed");
        }
            break;
        case ___ADS_TYPE___::BANNER:
        case ___ADS_TYPE___::INTERSTITIAL: {
            m_interAdLogs->setString("Inter ad Closed");
        }
            break;
        case ___ADS_TYPE___::APPOPEN:
            break;
    }
}

/*virtual*/void HelloWorld::___onAdFailed___(const ___ADS_TYPE___ pAdType, const ___FAIL_SUBEVENTS___ p_Event) /*override*/
{
    ___AdsHandler___::___getInstance___()->___showAdsFailPopUp___(nullptr);
}

void HelloWorld::___onAdCacheStatusChanged___(const ___ADS_TYPE___ pAdType, const bool isCashed) /*override*/
{

    switch(pAdType)
    {
        case ___ADS_TYPE___::VIDEO:
        {
            if (isCashed)
            {
                m_videoAdLogs->setString("Rewarded ad Available");
                m_showVideoAdItem->setVisible(true);
            }
            else
            {
                m_videoAdLogs->setString("Rewarded ad not Available");
                m_showVideoAdItem->setVisible(false);
            }
        }
            break;
        case ___ADS_TYPE___::APPOPEN:
        case ___ADS_TYPE___::INTERSTITIAL:
        {
            if (isCashed)
            {
                m_interAdLogs->setString("inter ad Available");
                m_showInterAdItem->setVisible(true);
            }
            else
            {
                m_interAdLogs->setString("inter ad not Available");
                m_showInterAdItem->setVisible(false);
            }
        }
            break;
        case ___ADS_TYPE___::BANNER:
        {
            if (isCashed)
            {
                m_bannerAdLogs->setString("Banner ad Available");
                m_showBannerAdItem->setVisible(true);
            }
            else
            {
                m_bannerAdLogs->setString("Banner ad not Available");
                m_showBannerAdItem->setVisible(false);
            }
        }
            break;
            break;
    }
}

void HelloWorld::addBackButtonListener()
{
    m_keyBoardListner = EventListenerKeyboard::create();
    m_keyBoardListner->onKeyReleased = CC_CALLBACK_2(HelloWorld::onKeyReleased, this);
    _eventDispatcher->addEventListenerWithSceneGraphPriority(m_keyBoardListner, this);
}

void HelloWorld::onKeyReleased(EventKeyboard::KeyCode keyCode, Event* event)
{
    if (keyCode == EventKeyboard::KeyCode::KEY_ESCAPE)
    {
        CCLOG("On back button pressed");
        m_backCount++;
        std::string buttonText = StringUtils::format("back button pressed for %i times", m_backCount);
        m_backbuttonLog->setString(buttonText.c_str());
        event->stopPropagation();
    }
}

