//
//  CommonModuleUtils.h
//  Common1
//
//  Created by Muhammad Arslan on 12/08/2015.
//
//

#ifndef Common1_CommonModuleUtils_h
#define Common1_CommonModuleUtils_h

#include "cocos2d.h"

#include "stdio.h"
#include "ui/CocosGUI.h"
#include "cocostudio/CocoStudio.h"
#include "json/document.h"
#include "../cpp/CommonLoadingLayer.h"
#include "../cpp/CommonModuleConstants.h"

#define USER_ID_KEY ("USER_UNIQUE_ID_KEY")

using namespace cocos2d;
using namespace cocos2d::ui;
enum ___ENetworkType___
{
    eNetworkMobile = 0,
    eNetworkWifi,
    eNetworkNone
};

enum ___ATTAuthorizationStatus___
{
    NotDetermined = 0,
    Restricted,
    Denied,
    Authorized
};



class ___CommonModuleUtils___
{
private:
    static std::string m_deviceUniqueIdentifier;
    static int m_currentSessionNumber;

public:
	static bool ___setupEasyNDK___(const char *packageName, const char* methodName, bool isStatic = false);
    static cocos2d::ValueMap ___getValueMapFromFile___(const std::string& filename);
    static bool ___isConnectedToNetwork___();
    static bool ___isGooglePlayServicesAvailable___();
    static ___ENetworkType___ ___getNetworkType___();
    static long ___getRamMemoryStatus___();
    static long ___getHeapMemoryStatus___();
    static long ___getTotalRamMemoryStatus___();
    static ___CommonLoadingLayer___ * ___getLoadingLayer___(const std::string initiatorName = "", std::function<void(void)> closeButtonCallback = nullptr);
    static std::string ___getDeviceUniqueIdentifier___();
    static std::string ___getDeviceOSVersion___();
    //getDevicePlatform will give ios, android or windows_phone
    static std::string ___getDevicePlatform___();
    //getDeploymentPlatform will give ios, amazon, android or windows_phone
    static std::string ___getDeviceManufacturer___();
    static std::string ___getDeviceModel___();
    static bool ___isDeviceOSVersionGreaterOrEqual___(const std::string& versionString);
    static ___ATTAuthorizationStatus___ ___getATTAuthorizationStatus___();
    static double ___getCurrentTimeInSeconds___();
    static std::string ___getCurrentDateString___();
    static int ___getGameSize___();
    static int ___getTotalDiskSize___();
    static int ___getRemainingDiskSize___();
    static const std::string ___getConfigsPath___();

    static bool ___containsDataInLocalBundle___(const std::string directoryPath);
    static std::string ___getStdStringWithFormat___(const char* format, ...);
    //static const std::string getFormattedStringFromNumber(double n);

    template <typename T>
    static void ___shuffleVector___(std::vector<T>& container) {
        static std::random_device rd;
        static std::mt19937 rng(rd());
        std::shuffle(container.begin(), container.end(), rng);
    }
};

#endif
