//
//  IAdListener.h
//  ModuleCommon
//
//  Created by Ashutosh Kumar Jha on 5/8/17.
//

#ifndef IAdListener_h
#define IAdListener_h

class ___IAdListener___
{
public:
    
    enum class ___FAIL_SUBEVENTS___
    {
        PLAY,
        LOAD,
    };
    
    enum class ___ADS_TYPE___
    {
        VIDEO,
        INTERSTITIAL,
        BANNER,
        APPOPEN
    };
    
    virtual ~___IAdListener___(){}
    ___IAdListener___(){}
    
    virtual void ___onAdStarted___(const ___ADS_TYPE___ pAdType){}
    
    virtual void ___onAdClosed___(const ___ADS_TYPE___ pAdType, bool giveReward){}
    
    virtual void ___onAdFailed___(const ___ADS_TYPE___ pAdType, const ___FAIL_SUBEVENTS___ p_Event){}
    
    virtual void ___onAdCacheStatusChanged___(const ___ADS_TYPE___ pAdType, const bool isCashed){}
};

#endif /* IAdListener_h */
