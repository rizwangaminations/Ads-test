//
//  NDKHelper.cpp
//  EasyNDK-for-cocos2dx
//
//  Created by Amir Ali Jiwani on 23/02/2013.
//  Updated by Alfonso Cejudo March, 2014.
//
//

#include "NDKHelper.h"
#include "CallFuncNV.h"
#if CC_TARGET_PLATFORM == CC_PLATFORM_WP8
#include "WP8NDKHelperBridge/WP8NDKHelperBridge.h"
#endif
USING_NS_CC;

#define __CALLED_METHOD__           "calling_method_name"
#define __CALLED_METHOD_PARAMS__    "calling_method_params"

std::vector<NDKCallbackNode> NDKHelper::selectorList;

void NDKHelper::addSelector(const char *groupName, const char *name, FuncNV selector, Node *target)
{
    NDKHelper::selectorList.push_back(NDKCallbackNode(groupName, name, selector, target));
}

void NDKHelper::printSelectorList()
{
    for (unsigned int i = 0; i < NDKHelper::selectorList.size(); ++i) {
        std::string s = NDKHelper::selectorList[i].getGroup();
        s.append(NDKHelper::selectorList[i].getName());
    }
}

void NDKHelper::removeSelectorsInGroup(const char *groupName)
{
    std::vector<int> markedIndices;
    
    for (unsigned int i = 0; i < NDKHelper::selectorList.size(); ++i) {
        if (NDKHelper::selectorList[i].getGroup().compare(groupName) == 0) {
            markedIndices.push_back(i);
        }
    }
    
    for (long i = markedIndices.size() - 1; i >= 0; --i) {
        NDKHelper::selectorList.erase(NDKHelper::selectorList.begin() + markedIndices[i]);
    }
}

cocos2d::Value NDKHelper::getValueFromJson(json_t *obj)
{
    if (obj == NULL) {
        return cocos2d::Value::Null;
    }
    
    if (json_is_object(obj)) {
        ValueMap valueMap;
        
        const char *key;
        json_t *value;
        
        void *iter = json_object_iter(obj);
        while (iter) {
            key = json_object_iter_key(iter);
            value = json_object_iter_value(iter);
            
            valueMap[key] = NDKHelper::getValueFromJson(value);
            
            iter = json_object_iter_next(obj, iter);
        }
        
        return cocos2d::Value(valueMap);
    } else if (json_is_array(obj)) {
        ValueVector valueVector;
        
        size_t sizeArray = json_array_size(obj);
        
        for (unsigned int i = 0; i < sizeArray; i++) {
            valueVector.push_back(NDKHelper::getValueFromJson(json_array_get(obj, i)));
        }
        
        return cocos2d::Value(valueVector);
    } else if (json_is_boolean(obj)) {
        if (json_is_true(obj)) {
            return cocos2d::Value(true);
        } else {
            return cocos2d::Value(false);
        }
    } else if (json_is_integer(obj)) {
        int value = (int) json_integer_value(obj);
        
        return cocos2d::Value(value);
    } else if (json_is_real(obj)) {
        double value = json_real_value(obj);
        
        return cocos2d::Value(value);
    } else if (json_is_string(obj)) {
        std::string value = json_string_value(obj);
        
        return cocos2d::Value(value);
    }
    
    return cocos2d::Value::Null;
}

json_t *NDKHelper::getJsonFromValue(cocos2d::Value value)
{
    if (value.getType() == cocos2d::Value::Type::MAP) {
        ValueMap valueMap = value.asValueMap();
        
        json_t *jsonDict = json_object();
        
        for (auto &element : valueMap) {
            json_object_set_new(jsonDict, element.first.c_str(),
                                NDKHelper::getJsonFromValue(element.second));
        }
        
        return jsonDict;
    } else if (value.getType() == cocos2d::Value::Type::VECTOR) {
        ValueVector valueVector = value.asValueVector();
        
        json_t *jsonArray = json_array();
        
        size_t sizeVector = valueVector.size();
        
        for (unsigned int i = 0; i < sizeVector; i++) {
            json_array_append_new(jsonArray,
                                  NDKHelper::getJsonFromValue(valueVector.at(i)));
        }
        
        return jsonArray;
    } else if (value.getType() == cocos2d::Value::Type::BOOLEAN) {
        return json_boolean(value.asBool());
    } else if (value.getType() == cocos2d::Value::Type::INTEGER) {
        return json_integer(value.asInt());
    } else if (value.getType() == cocos2d::Value::Type::DOUBLE) {
        return json_real(value.asDouble());
    } else if (value.getType() == cocos2d::Value::Type::STRING) {
        return json_string(value.asString().c_str());
    }
    
    return NULL;
}

void NDKHelper::handleMessage(json_t *methodName, json_t *methodParams)
{
    if (methodName == NULL) {
        return;
    }
    
    const char *methodNameStr = json_string_value(methodName);

#if CC_TARGET_PLATFORM == CC_PLATFORM_WP8

	const char *paramStr = json_string_value(methodParams);

	json_error_t jerror;
	json_t *jsonParameters = json_loads(paramStr, 0, &jerror);

	if (!jsonParameters) {
		fprintf(stderr, "error: on line %d: %s\n", jerror.line, jerror.text);
		return;
	}


#endif
    
    for (unsigned int i = 0; i < NDKHelper::selectorList.size(); ++i) {
        if (NDKHelper::selectorList[i].getName().compare(methodNameStr) == 0) {

#if CC_TARGET_PLATFORM == CC_PLATFORM_WP8
			Value value = NDKHelper::getValueFromJson(jsonParameters);
#else
			cocos2d::Value value = NDKHelper::getValueFromJson(methodParams);
#endif
            
            FuncNV sel = NDKHelper::selectorList[i].getSelector();
            Node *target = NDKHelper::selectorList[i].getTarget();
            
            CallFuncNV *caller = CallFuncNV::create(sel);
            caller->setValue(value);
            
            if (target) {
//                FiniteTimeAction *action = Sequence::create(caller, NULL);
//                
//                target->runAction(action);
                
                //Arslan::Commented above and calling function like below for avoiding addChild layer for getting callbacks
                sel((Node*)target , value);
            } else {
                caller->execute();
            }
            
//            break;
        }
    }
}

#if (CC_TARGET_PLATFORM == CC_PLATFORM_WP8)
void NDKHelper::CPPNativeCallHandler(Platform::String^ json)
{
	std::wstring strW(json->Begin());
	std::string jsonData = std::string(strW.begin(), strW.end());

	/*			const char *chars = jsonData.c_str();
	std::string ret(chars);
	env->ReleaseStringUTFChars(json, chars)*/;

	std::string jsonString = jsonData;
	/* End jstring2string code */

	const char *jsonCharArray = jsonString.c_str();

	json_error_t error;
	json_t *root;
	root = json_loads(jsonCharArray, 0, &error);

	if (!root) {
		fprintf(stderr, "error: on line %d: %s\n", error.line, error.text);
		return;
	}

	json_t *jsonMethodName, *jsonMethodParams;
	jsonMethodName = json_object_get(root, __CALLED_METHOD__);
	jsonMethodParams = json_object_get(root, __CALLED_METHOD_PARAMS__);

	// Just to see on the log screen if messages are propogating properly
	// __android_log_print(ANDROID_LOG_DEBUG, LOG_TAG, jsonCharArray);

	NDKHelper::handleMessage(jsonMethodName, jsonMethodParams);
	json_decref(root);
	}
#endif

#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)
#include "../../cocos2d/cocos/platform/android/jni/JniHelper.h"
#include <android/log.h>
#include <jni.h>

#define LOG_TAG    "EasyNDK-for-cocos2dx"
#define CLASS_NAME "com/easyndk/classes/AndroidNDKHelper"
#endif

#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
#import "IOSNDKHelper-C-Interface.h"
#endif

#if (CC_TARGET_PLATFORM == CC_PLATFORM_WP8)
Platform::String^ stringToPlatformString(std::string s)
{
	wchar_t *       pwszBuffer = nullptr;
	int num_chars = s.size();
	int nBufLen = num_chars + 1;
	pwszBuffer = new wchar_t[nBufLen];
	if (!pwszBuffer)
	{

	}
	memset(pwszBuffer, 0, nBufLen);
	num_chars = MultiByteToWideChar(CP_UTF8, 0, s.c_str(), num_chars, pwszBuffer, nBufLen);
	pwszBuffer[num_chars] = '\0';
	Platform::String^ p_string = ref new Platform::String(pwszBuffer);
	return p_string;
}
#endif

extern "C"
{
#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)
    // Method for receiving NDK messages from Java, Android
    void Java_com_easyndk_classes_AndroidNDKHelper_CPPNativeCallHandler(JNIEnv *env, jobject thiz, jstring json) {
        /* The JniHelper call resulted in crash, so copy the jstring2string method here */
        //std::string jsonString = JniHelper::jstring2string(json);
    	CCLOG("Success NDKHelper JNI");
        if (json == NULL) {
            return;
        }
        
        JNIEnv *pEnv = JniHelper::getEnv();
        if (!env) {
            return;
        }
        
        const char *chars = env->GetStringUTFChars(json, NULL);
        std::string ret(chars);
        env->ReleaseStringUTFChars(json, chars);
        
        std::string jsonString = ret;
        /* End jstring2string code */
        
        const char *jsonCharArray = jsonString.c_str();
        
        json_error_t error;
        json_t *root;
        root = json_loads(jsonCharArray, 0, &error);
        
        if (!root) {
            fprintf(stderr, "error: on line %d: %s\n", error.line, error.text);
            return;
        }
        
        json_t *jsonMethodName, *jsonMethodParams;
        jsonMethodName = json_object_get(root, __CALLED_METHOD__);
        jsonMethodParams = json_object_get(root, __CALLED_METHOD_PARAMS__);
        
        // Just to see on the log screen if messages are propogating properly
        // __android_log_print(ANDROID_LOG_DEBUG, LOG_TAG, jsonCharArray);
        
        NDKHelper::handleMessage(jsonMethodName, jsonMethodParams);
        json_decref(root);
    }
#endif
    
    // Method for sending message from CPP to the targeted platform
    void sendMessageWithParams(std::string methodName, cocos2d::Value methodParams, const char* ndkIdentifier) {
        if (0 == strcmp(methodName.c_str(), "")) {
            return;
        }
        
        json_t *toBeSentJson = json_object();
        json_object_set_new(toBeSentJson, __CALLED_METHOD__, json_string(methodName.c_str()));
        
        if (!methodParams.isNull()) {
            cocos2d::ValueMap valueMap = methodParams.asValueMap();
            valueMap["ndkIdentifier"] = ndkIdentifier;
            json_t *paramsJson = NDKHelper::getJsonFromValue(cocos2d::Value(valueMap));
            json_object_set_new(toBeSentJson, __CALLED_METHOD_PARAMS__, paramsJson);
        }
        else
        {
            cocos2d::ValueMap valueMap;
            valueMap["ndkIdentifier"] = ndkIdentifier;
            
            json_t *paramsJson = NDKHelper::getJsonFromValue(cocos2d::Value(valueMap));
            json_object_set_new(toBeSentJson, __CALLED_METHOD_PARAMS__, paramsJson);

        }
        
#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)
        JniMethodInfo t;
        
		if (JniHelper::getStaticMethodInfo(t,
                                           CLASS_NAME,
                                           "ReceiveCppMessage",
                                           "(Ljava/lang/String;)V")) {
            char *jsonStrLocal = json_dumps(toBeSentJson, JSON_COMPACT | JSON_ENSURE_ASCII);
            std::string jsonStr(jsonStrLocal);
            free(jsonStrLocal);
            
            jstring stringArg1 = t.env->NewStringUTF(jsonStr.c_str());
            t.env->CallStaticVoidMethod(t.classID, t.methodID, stringArg1);
            JniHelper::checkAndClearExceptions(t.env, CLASS_NAME, "ReceiveCppMessage");
            t.env->DeleteLocalRef(stringArg1);
			t.env->DeleteLocalRef(t.classID);
		}
#endif
        
#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS)
        json_t *jsonMessageName = json_string(methodName.c_str());
        
        if (!methodParams.isNull()) {
            json_t *jsonParams = NDKHelper::getJsonFromValue(methodParams);
            
            IOSNDKHelperImpl::receiveCPPMessage(jsonMessageName, jsonParams, ndkIdentifier);
            
            json_decref(jsonParams);
        } else {
            IOSNDKHelperImpl::receiveCPPMessage(jsonMessageName, NULL, ndkIdentifier);
        }
        
        json_decref(jsonMessageName);
#endif

#if (CC_TARGET_PLATFORM == CC_PLATFORM_WP8)

		/*wchar_t *       pwszBuffer = nullptr;
		int num_chars = methodName.size();
		int nBufLen = num_chars + 1;
		pwszBuffer = new wchar_t[nBufLen];
		if (!pwszBuffer)
		{

		}
		memset(pwszBuffer, 0, nBufLen);
		num_chars = MultiByteToWideChar(CP_UTF8, 0, methodName.c_str(), num_chars, pwszBuffer, nBufLen);
		pwszBuffer[num_chars] = '\0';
		Platform::String^ p_string = ref new Platform::String(pwszBuffer);*/
		Platform::String^ p_string = "";
		Platform::String^ m_string = stringToPlatformString(methodName);
		
		if (!methodParams.isNull()) {
			json_t *jsonParams = NDKHelper::getJsonFromValue(methodParams);

			if (jsonParams)
			{
				const char* paramStr = json_dumps(jsonParams, JSON_ENCODE_ANY);// json_string_value(jsonParams);

				if (strcmp(paramStr, "") != 0)
				{
					p_string = stringToPlatformString(paramStr);
				}
			}
		}

		

		WP8NDKHelperBridge::sharedInstance()->receiveCPPMessage(m_string, p_string);
#endif
        
        json_decref(toBeSentJson);
    }
}

