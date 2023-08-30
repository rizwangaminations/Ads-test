LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := moduleads_static

LOCAL_MODULE_FILENAME := libmoduleads

LOCAL_ARM_MODE := arm
LOCAL_SHORT_COMMANDS := true

CPP_ADS_MODULE_FILES  := $(wildcard $(LOCAL_PATH)/cpp/*.cpp)
CPP_ADS_MODULE_FILES  := $(CPP_ADS_MODULE_FILES:$(LOCAL_PATH)/%=%)

JANSSON_FILES  := $(wildcard $(LOCAL_PATH)/cpp/ThirdParty/NDKHelper/jansson/*.c)
JANSSON_FILES  := $(JANSSON_FILES:$(LOCAL_PATH)/%=%)

NDKHELPER_FILES  := $(wildcard $(LOCAL_PATH)/cpp/ThirdParty/NDKHelper/NDKHelper/*.cpp)
NDKHELPER_FILES  := $(NDKHELPER_FILES:$(LOCAL_PATH)/%=%)

HMAC_FILES  := $(wildcard $(LOCAL_PATH)/cpp/ThirdParty/hash-library/*.cpp)
HMAC_FILES  := $(HMAC_FILES:$(LOCAL_PATH)/%=%)

CNATIVE_FILES  := $(wildcard $(LOCAL_PATH)/android/src/com/modules/CNative/*.cpp)
CNATIVE_FILES  := $(CNATIVE_FILES:$(LOCAL_PATH)/%=%)


LOCAL_SRC_FILES := 	$(CPP_ADS_MODULE_FILES) \
					$(JANSSON_FILES) \
					$(NDKHELPER_FILES) \
					$(HMAC_FILES) \
				   	$(CNATIVE_FILES)


LOCAL_EXPORT_C_INCLUDES :=	$(LOCAL_PATH)/.. \
					       	$(LOCAL_PATH)/cpp \
							$(LOCAL_PATH)/cpp/ThirdParty/NDKHelper/NDKHelper \
							$(LOCAL_PATH)/cpp/ThirdParty/NDKHelper/jansson \
							$(LOCAL_PATH)/cpp/ThirdParty/hash-library \
							$(LOCAL_PATH)/android/src/com/modules/CNative \
							$(LOCAL_PATH)/cpp/ThirdParty/uuid-generator

LOCAL_C_INCLUDES := $(LOCAL_PATH)/.. \
					$(LOCAL_PATH)/cpp \
					$(LOCAL_PATH)/cpp/ThirdParty/NDKHelper/NDKHelper \
					$(LOCAL_PATH)/cpp/ThirdParty/NDKHelper/jansson \
					$(LOCAL_PATH)/cpp/ThirdParty/hash-library \
					$(LOCAL_PATH)/cpp/ThirdParty/uuid-generator


LOCAL_STATIC_LIBRARIES := cc_static
LOCAL_STATIC_LIBRARIES += ext_curl
LOCAL_STATIC_LIBRARIES += fairygui_static

include $(BUILD_STATIC_LIBRARY)

$(call import-module,.)
$(call import-module,../libfairygui)
$(call import-module,prebuilt/android)

