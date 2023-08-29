//
//  module-ads-include.h
//  Module-Ads
//
//  Created by Abdul Wasay on 12/08/2015.
//
//

#ifndef Module_Ads_module_ads_include_h
#define Module_Ads_module_ads_include_h

#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
#ifdef __OBJC__
    #import "ios/AdHandler.h"
#endif
#endif

#include "cpp/AdsHandler.h"
#include "cpp/AdNetworkModels.h"
#include "cpp/IAdListener.h"

#endif
