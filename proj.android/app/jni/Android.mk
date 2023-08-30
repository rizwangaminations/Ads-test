LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)


LOCAL_MODULE := cocos2dcpp

LOCAL_MODULE_FILENAME := libcocos2dcpp

CLASSES_FILES   := $(wildcard $(LOCAL_PATH)/../../../Classes/*.cpp)
CLASSES_FILES   := $(CLASSES_FILES:$(LOCAL_PATH)/%=%)

CLASSES_ADS_FILES   := $(wildcard $(LOCAL_PATH)/../../../moduleads/cpp/*.cpp)
CLASSES_ADS_FILES   := $(CLASSES_ADS_FILES:$(LOCAL_PATH)/%=%)

LOCAL_ARM_MODE := arm
LOCAL_SHORT_COMMANDS := true

LOCAL_SRC_FILES := hellocpp/main.cpp \
				   $(CLASSES_FILES) \
				   $(CLASSES_ADS_FILES)

LOCAL_EXPORT_C_INCLUDES :=	$(LOCAL_PATH)/.. \
						    $(LOCAL_PATH)/../../../cocos2d/cocos/network


LOCAL_C_INCLUDES := $(LOCAL_PATH)/../../../ \
					$(LOCAL_PATH)/../../../Classes \
					$(LOCAL_PATH)/../../../moduleads \
					$(LOCAL_PATH)/../../../cocos2d/external/curl/include/android


# _COCOS_HEADER_ANDROID_BEGIN
# _COCOS_HEADER_ANDROID_END


LOCAL_STATIC_LIBRARIES := cc_static
LOCAL_STATIC_LIBRARIES += ext_curl
LOCAL_STATIC_LIBRARIES += moduleads_static
LOCAL_STATIC_LIBRARIES += fairygui_static

# _COCOS_LIB_ANDROID_BEGIN
# _COCOS_LIB_ANDROID_END

include $(BUILD_SHARED_LIBRARY)

$(call import-module,.)
$(call import-module,../libfairygui)
$(call import-module,prebuilt/android)
$(call import-module,../../moduleads)
$(call import-module,../cocos2d/external/curl/prebuilt/android)

# _COCOS_LIB_IMPORT_ANDROID_BEGIN
# _COCOS_LIB_IMPORT_ANDROID_END
