//
//  CommonLoadingLayer.cpp
//  ModuleCommon
//
//  Created by Umair Javed on 20/11/2015.
//  Copyright © 2015 Gaminations. All rights reserved.
//

#include "CommonLoadingLayer.h"


___CommonLoadingLayer___ * ___CommonLoadingLayer___::create(const Color4B& color, std::function<void(void)> closeButtonCallback)
{
    
    ___CommonLoadingLayer___ * pObj = new (std::nothrow) ___CommonLoadingLayer___(closeButtonCallback);
    if( pObj && pObj->initWithColor(color) )
    {
        pObj->addLoading();
        pObj->autorelease();
        return pObj;
    }
    CC_SAFE_DELETE(pObj);
    return NULL;

}

___CommonLoadingLayer___::___CommonLoadingLayer___(std::function<void(void)> closeButtonCallback)
:   m_eventDispatcher(nullptr)
,   m_keyBoardListner(nullptr)
,   m_isBackButtonBlocked(false)
,   m_btnClose(nullptr)
,   m_closeButtonCallback(closeButtonCallback)
{
    addBackButtonListner();
}

___CommonLoadingLayer___::~___CommonLoadingLayer___()
{
    _eventDispatcher->removeEventListener(m_keyBoardListner);
    _eventDispatcher->removeEventListener(m_eventDispatcher);
}

void ___CommonLoadingLayer___::onEnter()
{
    LayerColor::onEnter();
    m_eventDispatcher = EventListenerTouchOneByOne::create();
    m_eventDispatcher->setSwallowTouches(true);
    m_eventDispatcher->onTouchBegan = CC_CALLBACK_2(___CommonLoadingLayer___::onTouchBegan, this);
    _eventDispatcher->addEventListenerWithSceneGraphPriority(m_eventDispatcher, this);
}

void ___CommonLoadingLayer___::onExit()
{
    Layer::onExit();
}

bool ___CommonLoadingLayer___::onTouchBegan(Touch *touch, Event *unusedEvent)
{
    return true;
}

void ___CommonLoadingLayer___::showCloseButton()
{
    if (m_btnClose)
    {
        m_btnClose->setVisible(true);
    }
}

void ___CommonLoadingLayer___::closeButtonPressed(cocos2d::Ref* pSender, cocos2d::ui::Widget::TouchEventType type)
{
    if (type == Widget::TouchEventType::ENDED)
    {
        m_closeButtonCallback();
    }
}

void ___CommonLoadingLayer___::addLoading()
{
    Size s = Director::getInstance()->getWinSize();
    SpriteFrameCache::getInstance()->addSpriteFramesWithFile(("CommonResource8.plist"));
    SpriteFrame *spinnerFrame = SpriteFrameCache::getInstance()->getSpriteFrameByName(("Common_loading_spinner.png"));
    Sprite *spinner = Sprite::createWithSpriteFrame(spinnerFrame);
    spinner->runAction(RepeatForever::create(RotateBy::create(0.5, 360)));
    addChild(spinner);
    spinner->setPosition(s/2);

    if (m_closeButtonCallback)
    {
        m_btnClose = cocos2d::ui::Button::create();
        m_btnClose->loadTextures(("LoadingScene_CloseButton.png"), ("LoadingScene_CloseButton.png"), ("LoadingScene_CloseButton.png"), ui::Widget::TextureResType::PLIST);
        m_btnClose->setPosition(s - (m_btnClose->getContentSize() * 0.5f));
        m_btnClose->setVisible(false);
        m_btnClose->addTouchEventListener(CC_CALLBACK_2(___CommonLoadingLayer___::closeButtonPressed, this));
        
        addChild(m_btnClose);
        
        DelayTime* delay = DelayTime::create(10.f);
        cocos2d::CallFunc* func = cocos2d::CallFunc::create(CC_CALLBACK_0(___CommonLoadingLayer___::showCloseButton,this));
        runAction(Sequence::create(delay,func, NULL));
    }
}

void ___CommonLoadingLayer___::addBackButtonListner()
{
    m_keyBoardListner = EventListenerKeyboard::create();
    m_keyBoardListner->onKeyReleased = CC_CALLBACK_2(___CommonLoadingLayer___::onKeyReleased, this);
    _eventDispatcher->addEventListenerWithSceneGraphPriority(m_keyBoardListner, this);
}

void ___CommonLoadingLayer___::onKeyReleased(EventKeyboard::KeyCode keyCode, Event* event)
{
    if (keyCode == EventKeyboard::KeyCode::KEY_ESCAPE && m_isBackButtonBlocked)
    {
        if (m_closeButtonCallback)
        {
            m_closeButtonCallback();
        }
        event->stopPropagation();
    }
}

