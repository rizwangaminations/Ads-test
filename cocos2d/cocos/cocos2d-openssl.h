//
//  cocos2d-openssl.h
//
//  Created by Boby Ilea on 15/09/2018.
//

#ifndef __COCOS2D_OPENSSL_H__
#define __COCOS2D_OPENSSL_H__

#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
    #include "external/openssl/include/ios/openssl/crypto.h"
    #include "external/openssl/include/ios/openssl/pkcs7.h"
    #include "external/openssl/include/ios/openssl/sha.h"
    #include "external/openssl/include/ios/openssl/x509.h"
    #include "external/openssl/include/ios/openssl/objects.h"
    //#include "external/openssl/include/ios/openssl/asn1.h"
    //#include "external/openssl/include/ios/openssl/bn.h"
    //#include "external/openssl/include/ios/openssl/asn1_locl.h"
#endif // CC_TARGET_PLATFORM == CC_PLATFORM_IOS

    #include "external/openssl/include/android/openssl/crypto.h"
#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)

#endif // CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID

#endif // __COCOS2D_OPENSSL_H__
