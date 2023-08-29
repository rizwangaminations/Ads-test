//
//  CallFuncNV.h
//  MechaDragoon
//
//  Created by Alfonso Cejudo on 3/15/14.
//
//

#ifndef __MechaDragoon__CallFuncNV__
#define __MechaDragoon__CallFuncNV__

#include "cocos2d.h"
#include "json/document.h"


using namespace rapidjson;
#if CC_TARGET_PLATFORM == CC_PLATFORM_WP8 || CC_TARGET_PLATFORM == CC_PLATFORM_WINRT
class __declspec(dllexport) CallFuncNV : public cocos2d::CallFunc
#else
class CC_DLL CallFuncNV : public cocos2d::CallFunc
#endif
{
public:
    static CallFuncNV *create(const std::function<void(cocos2d::Node *, cocos2d::Value)> &func);
    
    void setValue(cocos2d::Value value);
    void setValue(rapidjson::Value value);
    
    //
    // Overrides
    //
	virtual CallFuncNV *clone() const override;
    virtual void execute() override;
    
protected:
    CallFuncNV()
    : _functionNV(nullptr)
    {
    }
    virtual ~CallFuncNV(){}
    
    bool initWithFunction(const std::function<void(cocos2d::Node *, cocos2d::Value)> &func);
    
    std::function<void(cocos2d::Node *, cocos2d::Value)> _functionNV;
    cocos2d::Value _value;
    rapidjson::Value _rapidJsonValue;
    
private:
    CC_DISALLOW_COPY_AND_ASSIGN(CallFuncNV);
};

#endif /* defined(__MechaDragoon__CallFuncNV__) */
