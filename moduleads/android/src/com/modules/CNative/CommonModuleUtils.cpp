//
//  CommonModuleUtils.cpp
//  Common1
//
//  Created by Muhammad Arslan on 12/08/2015.
//
//

#include "CommonModuleUtils.h"
#include "../../moduleads/cpp/CommonModule.h"
#include "../../cocos2d/cocos/platform/android/jni/JniHelper.h"
#include <jni.h>

#define CURRENT_SESSION_NUMBER_KEY declare_str("CommonModuleUtils:CURRENT_SESSION_NUMBER_KEY")
#define kMaxStringLen (1024*100)
#define HDR_LOWDISK_TRESHOLD 400
#define HD_LOWDISK_TRESHOLD 200
#define SD_LOWDISK_TRESHOLD 100

std::string ___CommonModuleUtils___::m_deviceUniqueIdentifier = "";

bool ___CommonModuleUtils___::___setupEasyNDK___(const char *packageName, const char* methodName, bool isStatic)
{
    if(strcmp(packageName, "") == 0)
    {
        return false;
    }

    if(isStatic)
    {
        cocos2d::JniMethodInfo t;
        if (cocos2d::JniHelper::getStaticMethodInfo(t, packageName, methodName, "()V"))
        {

            t.env->CallStaticVoidMethod(t.classID, t.methodID);
            JniHelper::checkAndClearExceptions(t.env, packageName, methodName);
            t.env->DeleteLocalRef(t.classID);
        }
    }
    else
    {
        JNIEnv *env = JniHelper::getEnv();
        if (!env)
        {
            return false;
        }

        jclass globalClass = env->FindClass(packageName);
        if (! globalClass)
        {
            CCLOG("Failed to create class Obj");
            return false;
        }
        CCLOG("Success1");
        jmethodID mid = env->GetMethodID(globalClass, methodName, "()V");
        if (!mid)
        {
            CCLOG("Failed to create method id Obj");
            return false;
        }
        jobject intent = env->AllocObject(globalClass);

        env->CallVoidMethod(intent, mid);
        JniHelper::checkAndClearExceptions(env, packageName, methodName);
    }
    return true;
}

bool ___CommonModuleUtils___::___isDeviceOSVersionGreaterOrEqual___(const std::string& versionString)
{
    //TODO:: Implement When Needed!
    return false;
}

___ATTAuthorizationStatus___ ___CommonModuleUtils___::___getATTAuthorizationStatus___()
{
    return ___ATTAuthorizationStatus___::Restricted;
}

std::string ___CommonModuleUtils___::___getDeviceManufacturer___()
{
    const char *packageName = "com/modules/common/CommonModuleUtils";
    const char *methodName = "getDeviceManufacturer";

    cocos2d::JniMethodInfo methodInfo;

    if (!cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName,
                                                 "()Ljava/lang/String;"))
    {
        return "";
    }

    jstring versionJStr = (jstring) methodInfo.env->CallStaticObjectMethod(methodInfo.classID,
                                                                           methodInfo.methodID);
    bool hasException = JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);

    std::string versionStr;

    if (!hasException)
    {
        versionStr = JniHelper::jstring2string(versionJStr);
    }

    methodInfo.env->DeleteLocalRef(methodInfo.classID);
    methodInfo.env->DeleteLocalRef(versionJStr);

    return versionStr;
}

std::string ___CommonModuleUtils___::___getDevicePlatform___()
{
    return std::string("android");
}

std::string ___CommonModuleUtils___::___getDeviceModel___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "getDeviceModel";

    cocos2d::JniMethodInfo methodInfo;

    if (!cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()Ljava/lang/String;"))
    {
        return "";
    }

    jstring deviceModelJStr = (jstring)methodInfo.env->CallStaticObjectMethod(methodInfo.classID, methodInfo.methodID);
    bool hasException = JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);

    std::string deviceModelStr;
    if (!hasException)
    {
        deviceModelStr = JniHelper::jstring2string(deviceModelJStr);
    }

    methodInfo.env->DeleteLocalRef(methodInfo.classID);
    methodInfo.env->DeleteLocalRef(deviceModelJStr);

    return deviceModelStr;
}

std::string ___CommonModuleUtils___::___getDeviceOSVersion___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "getDeviceOSVersion";

    cocos2d::JniMethodInfo methodInfo;

    if (! cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()Ljava/lang/String;"))
    {
        return "";
    }

    jstring deviceOSJStr = (jstring)methodInfo.env->CallStaticObjectMethod(methodInfo.classID, methodInfo.methodID);
    bool hasException = JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);

    std::string deviceOSStr;
    if (!hasException)
    {
        deviceOSStr = JniHelper::jstring2string(deviceOSJStr);
    }

    methodInfo.env->DeleteLocalRef(methodInfo.classID);
    methodInfo.env->DeleteLocalRef(deviceOSJStr);

    return deviceOSStr;
}

bool ___CommonModuleUtils___::___isGooglePlayServicesAvailable___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "isGooglePlayServicesAvailable";
    cocos2d::JniMethodInfo methodInfo;
    if (! cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()Z"))
    {
        return false;
    }
    const bool isAvailable = (bool) methodInfo.env->CallStaticBooleanMethod(methodInfo.classID, methodInfo.methodID);
    JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);
    methodInfo.env->DeleteLocalRef(methodInfo.classID);
    CCLOG("is play services available: %d", isAvailable);
    return isAvailable;
}

std::string ___CommonModuleUtils___::___getDeviceUniqueIdentifier___()
{
    if (m_deviceUniqueIdentifier.empty())
    {
        const char* packageName = "com/modules/common/CommonModuleUtils";
        const char* methodName = "getDeviceUniqueIdentifier";

        JNIEnv *env = JniHelper::getEnv();
        if (!env)
        {
            return "";
        }

        jclass globalClass = env->FindClass(packageName);
        if (! globalClass)
        {
            CCLOG("Failed to create class Obj");
            return "";
        }
        CCLOG("Success1");
        jmethodID mid = env->GetMethodID(globalClass, methodName , "()Ljava/lang/String;");
        if (!mid)
        {
            CCLOG("Failed to create method id Obj");
            return "";
        }
        jobject intent = env->AllocObject(globalClass);

        jstring versionJStr = (jstring)env->CallObjectMethod(intent, mid);
        bool hasException = JniHelper::checkAndClearExceptions(env, packageName, methodName);

        if (!hasException)
        {
            m_deviceUniqueIdentifier= JniHelper::jstring2string(versionJStr);
        }
        env->DeleteLocalRef(versionJStr);
    }
    return m_deviceUniqueIdentifier;
}

long ___CommonModuleUtils___::___getRamMemoryStatus___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "getRamMemoryStatus";

    cocos2d::JniMethodInfo methodInfo;

    if (!cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()J"))
    {
        return -1;
    }

    const long memInMB = (long) methodInfo.env->CallStaticLongMethod(methodInfo.classID, methodInfo.methodID);
    JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);
    methodInfo.env->DeleteLocalRef(methodInfo.classID);
    CCLOG("RAM memory available in MB %ld", memInMB);
    return memInMB;
}

long ___CommonModuleUtils___::___getHeapMemoryStatus___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "getHeapMemoryStatus";

    cocos2d::JniMethodInfo methodInfo;

    if (!cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()J"))
    {
        return -1;
    }

    const long memInMB = (long) methodInfo.env->CallStaticLongMethod(methodInfo.classID, methodInfo.methodID);
    JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);
    methodInfo.env->DeleteLocalRef(methodInfo.classID);
    CCLOG("Heap Memory available in MB %ld", memInMB);
    return memInMB;
}

long ___CommonModuleUtils___::___getTotalRamMemoryStatus___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "getTotalRamMemoryStatus";

    cocos2d::JniMethodInfo methodInfo;

    if (!cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()J"))
    {
        return -1;
    }

    const long memInMB = (long) methodInfo.env->CallStaticLongMethod(methodInfo.classID, methodInfo.methodID);
    JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);
    methodInfo.env->DeleteLocalRef(methodInfo.classID);
    CCLOG("Total RAM Memory available in MB %ld", memInMB);
    return memInMB;
}

___ENetworkType___ ___CommonModuleUtils___::___getNetworkType___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "getNetworkType";

    cocos2d::JniMethodInfo methodInfo;

    if (! cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()I"))
    {
        return eNetworkNone;
    }

    int networkType = (int) methodInfo.env->CallStaticIntMethod(methodInfo.classID, methodInfo.methodID);
    JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);
    methodInfo.env->DeleteLocalRef(methodInfo.classID);
    CCLOG("networkType: %d", networkType);

    return (___ENetworkType___) networkType;
}

int ___CommonModuleUtils___::___getGameSize___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "getGameSize";

    cocos2d::JniMethodInfo methodInfo;

    if (! cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()I"))
    {
        return -1;
    }

    const int sizeInMB = (int)methodInfo.env->CallStaticIntMethod(methodInfo.classID, methodInfo.methodID);
    JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);
    methodInfo.env->DeleteLocalRef(methodInfo.classID);

    return sizeInMB;
}

bool ___CommonModuleUtils___::___containsDataInLocalBundle___(const std::string folderPath)
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "containsDataInLocalBundle";
    cocos2d::JniMethodInfo methodInfo;
    if (! cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "(Ljava/lang/String;)Z"))
    {
        return false;
    }
    jstring convertedPath = methodInfo.env->NewStringUTF(folderPath.c_str());
    const bool dataExist = (bool)methodInfo.env->CallStaticBooleanMethod(methodInfo.classID, methodInfo.methodID, convertedPath);
    JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);
    methodInfo.env->DeleteLocalRef(methodInfo.classID);
    methodInfo.env->DeleteLocalRef(convertedPath);
    return dataExist;
}

int ___CommonModuleUtils___::___getTotalDiskSize___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "getTotalDiskSpace";

    cocos2d::JniMethodInfo methodInfo;

    if (! cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()I"))
    {
        return -1;
    }

    const int sizeInMB = (int)methodInfo.env->CallStaticIntMethod(methodInfo.classID, methodInfo.methodID);
    JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);
    methodInfo.env->DeleteLocalRef(methodInfo.classID);

    return sizeInMB;
}

int ___CommonModuleUtils___::___getRemainingDiskSize___()
{
    const char* packageName = "com/modules/common/CommonModuleUtils";
    const char* methodName = "getFreeDiskSpace";

    cocos2d::JniMethodInfo methodInfo;

    if (! cocos2d::JniHelper::getStaticMethodInfo(methodInfo, packageName, methodName, "()I"))
    {
        return -1;
    }

    const int sizeInMB = (int)methodInfo.env->CallStaticIntMethod(methodInfo.classID, methodInfo.methodID);
    JniHelper::checkAndClearExceptions(methodInfo.env, packageName, methodName);
    methodInfo.env->DeleteLocalRef(methodInfo.classID);

    return sizeInMB;
}

bool ___CommonModuleUtils___::___isConnectedToNetwork___()
{
    return ___CommonModule___::___getIsInternetConnected___();
}

double ___CommonModuleUtils___::___getCurrentTimeInSeconds___()
{
    time_t rawtime;
    time(&rawtime);
    long curTime = rawtime;

    return curTime;
}

/*static*/ std::string ___CommonModuleUtils___::___getCurrentDateString___()
{
    time_t currentTime;
    time (&currentTime);
    struct tm currentTimeStruct;
    currentTimeStruct = *gmtime(&currentTime);
    const int currentDay = currentTimeStruct.tm_mday;
    const int currentMonth = currentTimeStruct.tm_mon;
    const int currentYear = currentTimeStruct.tm_year;

    const std::string dateString = ___CommonModuleUtils___::___getStdStringWithFormat___(("%d_%d_%d"),currentDay,currentMonth,currentYear);
    return dateString;
}

std::string ___CommonModuleUtils___::___getStdStringWithFormat___(const char* format, ...)
{

    std::string result = "";

    va_list ap;
    va_start(ap, format);
    char* pBuf = (char*)malloc(kMaxStringLen);
    if (pBuf != nullptr)
    {
        vsnprintf(pBuf, kMaxStringLen, format, ap);
        result.append(pBuf);
        free(pBuf);
    }
    else{
        //CCLOG("issue");

    }
    va_end(ap);
    return result;
}

/*static*/ const std::string ___CommonModuleUtils___::___getConfigsPath___()
{
    return FileUtils::getInstance()->getWritablePath() + ("Configs/");
}

___CommonLoadingLayer___ * ___CommonModuleUtils___::___getLoadingLayer___(const std::string initiatorName, std::function<void(void)> closeButtonCallback)
{
    return ___CommonLoadingLayer___::create(Color4B(0,2,12,180), closeButtonCallback);
}

/*static*/ cocos2d::ValueMap ___CommonModuleUtils___::___getValueMapFromFile___(const std::string& filename)
{
    ValueMap valueMap;
    try
    {
        valueMap = FileUtils::getInstance()->getValueMapFromFile(filename);
    }
    catch(...)
    {
    }
    return valueMap;
}
