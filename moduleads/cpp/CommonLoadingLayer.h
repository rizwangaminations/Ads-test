//
//  CommonLoadingLayer.h
//  ModuleCommon
//
//  Created by Umair Javed on 20/11/2015.
//  Copyright © 2015 Gaminations. All rights reserved.
//

#ifndef CommonLoadingLayer_hpp
#define CommonLoadingLayer_hpp

#include <stdio.h>
#include "cocos2d.h"
#include "ui/CocosGUI.h"

using namespace cocos2d;
using namespace cocos2d::ui;

class ___CommonLoadingLayer___ : public cocos2d::LayerColor
{
private:
    virtual void onEnter();
    virtual void onExit();
    virtual bool onTouchBegan(Touch *touch, Event *unusedEvent);
    EventListenerTouchOneByOne*   m_eventDispatcher;
    EventListenerKeyboard*        m_keyBoardListner;
    bool                          m_isBackButtonBlocked;
    std::function<void(void)>     m_closeButtonCallback;
    
    void addLoading();
    void addBackButtonListner();
    void onKeyReleased(EventKeyboard::KeyCode keyCode, Event* event);
    void showCloseButton();
    void closeButtonPressed(cocos2d::Ref* pSender, cocos2d::ui::Widget::TouchEventType type);
    
    cocos2d::ui::Button*          m_btnClose;
public:
    inline void shouldBlockBackButton(const bool isBackButtonBlocked) { m_isBackButtonBlocked = isBackButtonBlocked; } ;
    ___CommonLoadingLayer___(std::function<void(void)> closeButtonCallback = nullptr);
    ~___CommonLoadingLayer___();
    static ___CommonLoadingLayer___ * create(const Color4B& color = Color4B(0,2,12,180), std::function<void(void)> closeButtonCallback = nullptr);
};


#endif /* CommonLoadingLayer_hpp */
