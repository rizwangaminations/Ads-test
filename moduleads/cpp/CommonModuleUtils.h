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
    static bool ___writeToFile___(const char * pszPath, const char *pData, size_t size);
    static cocos2d::Value ___convertDocumentToCObject___(const char* data);
    static cocos2d::ValueMap ___getValueMapFromFile___(const std::string& filename);
    static std::string ___getResourcePath___();
    static std::string ___getFilePath___();
    static bool ___isConnectedToNetwork___();
    static bool ___isGooglePlayServicesAvailable___();
    static ___ENetworkType___ ___getNetworkType___();
    static long ___getRamMemoryStatus___();
    static long ___getHeapMemoryStatus___();
    static long ___getTotalRamMemoryStatus___();
    static int ___autofitString___(Text* text);
    static int ___autofitString___(TextBMFont* text);
    static cocos2d::Node* ___getBoundsNode___(cocos2d::Node* node);
    static cocos2d::Size ___getTextBounds___(TextBMFont* const text);
    static void ___autofitStringInBounds___(TextBMFont* const text, const float margin = 0.0f);
    static void ___setButtonLabel___(Button* const button, const std::string& label);
    static void ___setButtonLocalizedLabel___(Button* const button, const std::string& localizationKey);
    static void ___autofitString___(TextBMFont* const text, const cocos2d::Size& container, const float margin);
    static std::string ___durationToString___(const long long seconds, bool makeExact = true);
    static void ___moveToTextLeftCorner___(cocos2d::ui::TextBMFont* text, Node* node);
    static void ___setCaptionAndBreakLinesInBounds___(cocos2d::ui::TextBMFont* label, const std::string& originalText);
    static void ___setCaptionAndBreakLines___(cocos2d::ui::TextBMFont* label, const std::string& originalText,
                                                    const cocos2d::Size& bounds);
    static void ___setLocalizedCaptionAndFitBounds___(cocos2d::ui::TextBMFont* text, const std::string& localizationKey,
                                                const bool alignToCenter = false);
    static void ___setCaptionAndFitBounds___(cocos2d::ui::TextBMFont* text, const std::string& caption,
                                       const bool alignToCenter = false);
    static void ___configureVIPInformationUI___(const cocos2d::Node* const parent, const std::string& iapName);
    static void ___configureVIPBenefitUI___(const cocos2d::Node* const parent);
    static void ___configureVIPElementUI___(const cocos2d::Node* const parent, const std::string& iapName);
    static void ___configureLocalizedTextField___(const cocos2d::Node* const parent,
                                            const std::string& childName,
                                            const std::string& localizationKey);
    static void ___autofitStringAndMaintainScale___(TextBMFont* text, cocos2d::Size containerSize, float margin);
    static void ___fitNodeInside___(cocos2d::Node* nodeToFit, const cocos2d::Size& nodeSize, const cocos2d::Size& areaToFitIn);
    static void ___setTextBMFontHorizntalTextAlignment___(TextBMFont* const textfield, const TextHAlignment alignment);
    static void ___setTextBMFontVerticalTextAlignment___(TextBMFont* const textfield, const TextVAlignment alignment);
    static bool ___replace___(std::string& str, const std::string& from, const std::string& to);
    static ___CommonLoadingLayer___ * ___getLoadingLayer___(const std::string initiatorName = "", std::function<void(void)> closeButtonCallback = nullptr);
    static std::string ___getIDFV___();
    static std::string ___getDeviceUniqueIdentifier___();
    static void ___setDeviceUniqueIdentifier___(const std::string userID);
    static std::string ___getDeviceOSVersion___();
    //getDevicePlatform will give ios, android or windows_phone
    static std::string ___getDevicePlatform___();
    //getDeploymentPlatform will give ios, amazon, android or windows_phone
    static std::string ___getDeploymentPlatform___();
    static std::string ___getFormattedTimeString___(int seconds);
    static std::string ___getFormattedTimeStringInMinutesAndSeconds___(int seconds);
    static std::string ___getFormattedTimeShortestString___(int seconds);
    static std::string ___getTimerString___(const double secondsRemaining,
                                      const std::string& dayString = ("%d day"),
                                      const std::string& daysString = ("%d days"));
    static std::string ___getDurationLongString___(const int durationMinutes);
    static std::string ___getDurationShortString___(const int durationMinutes);
    static std::string ___getDeviceManufacturer___();
    static std::string ___getDeviceModel___();
    static bool ___isDeviceOSVersionGreaterOrEqual___(const std::string& versionString);
    static ___ATTAuthorizationStatus___ ___getATTAuthorizationStatus___();
    static void ___setupCurrentSessionNumber___();
    static int ___getCurrentSessionNumber___();
    static double ___getCurrentTimeInSeconds___();
    static int ___getCurrentDayCount___();
    static int ___getCurrentWeekCount___();
    static std::string ___getCurrentDateString___();
    static std::string ___getCurrentDateTimeString___();
    static Vec2 ___getGlobalScale___(const cocos2d::Node* node);
    static bool ___isImageValid___(const std::string& imagePath);
    static int ___getLowDiskSpaceTreshold___();
    static int ___getGameSize___();
    static int ___getTotalDiskSize___();
    static int ___getRemainingDiskSize___();
    static bool ___isDeviceWithBottomBar___();
    static rapidjson::Document ___parseJsonString___(const std::string& jsonStr);
    static void ___setAppropriateFileServerURL___(std::string& urlString, const std::string& parseURL, const std::string& filePath);
    static std::string ___getUrlForFile___(const std::string& fileKey
                                     , cocos2d::ValueMap& valueMap
                                     , const std::string& basePath
                                     , const std::string& fileExtension
                                     , bool checkNative);
    static const std::string ___getConfigsPath___();
    static bool ___isDirectory___(const std::string& path);
    static std::string ___getDirectoryPath___(const std::string fileFullPath);

    static bool ___containsDataInLocalBundle___(const std::string directoryPath);
#pragma mark string utils
    static std::string ___getStringFromInt___(int value);
    static std::string ___getStringFromfloat___(float value);
    static std::string ___getStringFromFloatWithPrecision___(const float value, const int precision, const bool filterDotZero);
    static std::string ___getStringFromLong___(long value);
    static std::string ___getStringFromLongLong___(long long value);
    static std::string ___getStringFromDouble___(double value);
    static std::string ___getStdStringWithFormat___(const char* format, ...);
    static std::string ___getStringFromPoint___(cocos2d::Point point);
    //static const std::string getFormattedStringFromNumber(double n);
    static const double ___getNumberFromFormattedString___(std::string stringVal);
    static std::vector<std::string> ___tokenizeString___(const std::string& stringToSplit, const std::string& delimeter);
    static std::string ___toLower___(const std::string& stringToLower);
    static std::string ___toUpper___(const std::string& stringToUpper);
    static std::string ___removeUniCode___(const std::string& message);
    static void ___replaceStringInPlace___(std::string& subject, const std::string& search, const std::string& replace);
    static void ___evaluateString___(std::string& evaluateString, int numberOfParams, ...);
    static bool ___isUnSignedInt___(const std::string& message);

    static bool ___strIcompare___(const std::string& str1, const std::string& str2);
    static float ___getFloatFromPriceString___(const std::string& priceString);
    static void ___setEnabled___ (cocos2d::ui::Widget* widget, const bool isEnabled, const Color3B color = DISABLE_BUTTON_COLOR);
    
    static void ___applyTouchEventScale___(cocos2d::Ref* sender, cocos2d::ui::Widget::TouchEventType touchEventType,
                                   const float scaleFactor = 0.9f);
    static void ___applyTouchEventScaleIfNeeded___(cocos2d::Ref* sender, cocos2d::ui::Widget::TouchEventType touchEventType,
                                             const float scaleFactor = 0.9f);
    static void ___readjustChildrens___(Node* parentNode, const int padding = 20);
    
    static std::string ___getPackageNameForActiveSkin___(const std::string& packageName);
#pragma mark randomizer utils
    static int ___getRandomInt___(const int low, const int high);

    template <typename T>
    static void ___shuffleVector___(std::vector<T>& container)
    {
        static std::random_device rd;
        static std::mt19937 rng(rd());
        std::shuffle(container.begin(), container.end(), rng);
    }
    
    static long long ___daysToSeconds___(const long long nDays);
    static bool ___isTablet___();
    static void ___setGlobalZOrderRecursive___(cocos2d::Node *parent, float z);
    static float ___getScaleRecursive___(cocos2d::Node* node);

};

#endif
