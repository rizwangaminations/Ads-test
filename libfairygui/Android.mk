LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := fairygui_static

LOCAL_MODULE_FILENAME := libfairygui

LOCAL_ARM_MODE := arm

CPP_FAIRYGUI_MODULE_FILES  := $(wildcard $(LOCAL_PATH)/Classes/*.cpp)
CPP_FAIRYGUI_MODULE_FILES  := $(CPP_FAIRYGUI_MODULE_FILES:$(LOCAL_PATH)/%=%)

CONTROLLER_FILES  := $(wildcard $(LOCAL_PATH)/Classes/controller_action/*.cpp)
CONTROLLER_FILES  := $(CONTROLLER_FILES:$(LOCAL_PATH)/%=%)

DISPLAY_FILES  := $(wildcard $(LOCAL_PATH)/Classes/display/*.cpp)
DISPLAY_FILES  := $(DISPLAY_FILES:$(LOCAL_PATH)/%=%)

EVENT_FILES  := $(wildcard $(LOCAL_PATH)/Classes/event/*.cpp)
EVENT_FILES  := $(EVENT_FILES:$(LOCAL_PATH)/%=%)

GEARS_FILES  := $(wildcard $(LOCAL_PATH)/Classes/gears/*.cpp)
GEARS_FILES  := $(GEARS_FILES:$(LOCAL_PATH)/%=%)

TWEEN_FILES  := $(wildcard $(LOCAL_PATH)/Classes/tween/*.cpp)
TWEEN_FILES  := $(TWEEN_FILES:$(LOCAL_PATH)/%=%)

UTILS_FILES  := $(wildcard $(LOCAL_PATH)/Classes/utils/*.cpp)
UTILS_FILES  := $(UTILS_FILES:$(LOCAL_PATH)/%=%)

LOCAL_SRC_FILES := $(CPP_FAIRYGUI_MODULE_FILES) \
				   $(CONTROLLER_FILES) \
				   $(DISPLAY_FILES) \
                   $(EVENT_FILES) \
                   $(GEARS_FILES) \
				   $(TWEEN_FILES) \
				   $(UTILS_FILES)


LOCAL_CPP_FEATURES := rtti exceptions

LOCAL_STATIC_LIBRARIES := cc_static

LOCAL_EXPORT_C_INCLUDES := $(LOCAL_PATH)/Classes

LOCAL_C_INCLUDES := $(LOCAL_PATH)/Classes
                                 
include $(BUILD_STATIC_LIBRARY)
