LOCAL_PATH := $(call my-dir)
COCOS_ROOT_1 := $(LOCAL_PATH)/../../../cocos2d

include $(CLEAR_VARS)
LOCAL_MODULE := cocos_static
LOCAL_MODULE_FILENAME := libccstatic

LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/cocos                               \
                           $(COCOS_ROOT_1)/cocos/.                             \
						   $(COCOS_ROOT_1)/cocos/..                            \
						   $(COCOS_ROOT_1)/cocos/2d                            \
						   $(COCOS_ROOT_1)/cocos/audio/include                 \
						   $(COCOS_ROOT_1)/cocos/base                          \
						   $(COCOS_ROOT_1)/cocos/editor-support                \
						   $(COCOS_ROOT_1)/cocos/math                          \
						   $(COCOS_ROOT_1)/cocos/physics                       \
						   $(COCOS_ROOT_1)/cocos/platform                      \
						   $(COCOS_ROOT_1)/cocos/platform/android              \
						   $(COCOS_ROOT_1)/cocos/ui                            \
						   $(COCOS_ROOT_1)/external                            \
						   $(COCOS_ROOT_1)/external/Box2D                      \
                           $(COCOS_ROOT_1)/external/bullet/include/bullet      \
						   $(COCOS_ROOT_1)/external/chipmunk/include/chipmunk  \
						   $(COCOS_ROOT_1)/external/clipper                    \
						   $(COCOS_ROOT_1)/external/curl/include/android       \
						   $(COCOS_ROOT_1)/external/flatbuffers                \
						   $(COCOS_ROOT_1)/external/freetype2                  \
						   $(COCOS_ROOT_1)/external/poly2tri                   \
						   $(COCOS_ROOT_1)/external/poly2tri/common            \
						   $(COCOS_ROOT_1)/external/poly2tri/sweep             \
						   $(COCOS_ROOT_1)/external/tinyxml2                   \
						   $(COCOS_ROOT_1)/external/unzip                      \
						   $(COCOS_ROOT_1)/external/websockets/include/android \
						   $(COCOS_ROOT_1)/external/xxhash                     \
						   $(COCOS_ROOT_1)/external/xxtea                      \
						   $(COCOS_ROOT_1)/extensions


LOCAL_CFLAGS   :=  -DUSE_FILE32API -fexceptions

LOCAL_CPPFLAGS := -Wno-deprecated-declarations -Wno-extern-c-compat

LOCAL_EXPORT_CFLAGS   := -DUSE_FILE32API -fexceptions

LOCAL_EXPORT_CPPFLAGS := -Wno-deprecated-declarations -Wno-extern-c-compat

LOCAL_EXPORT_LDLIBS := -lGLESv2    \
                       -llog       \
                       -landroid   \
                       -lGLESv1_CM \
                       -lEGL       \
                       -lOpenSLES


LOCAL_WHOLE_STATIC_LIBRARIES := box2d_static
LOCAL_WHOLE_STATIC_LIBRARIES += bullet_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_chipmunk_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_curl_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_freetype2_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_jpeg_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_crypto_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_ssl_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_png_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_tiff_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_webp_static
LOCAL_WHOLE_STATIC_LIBRARIES += websockets_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_zlib_static

#下面就是自己用cocos gen-libs -c产生的静态库的添加
#总共构建17个库，这里添加，同时上面头文件路径也要添加
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_flatbuffers_static
LOCAL_WHOLE_STATIC_LIBRARIES += audioengine_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos2dx_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos2dxandroid_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos2dx_internal_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos3d_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocosbuilder_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocosdenshion_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocostudio_static
LOCAL_WHOLE_STATIC_LIBRARIES += cpufeatures_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_extension_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_network_static
LOCAL_WHOLE_STATIC_LIBRARIES += libpvmp3dec
LOCAL_WHOLE_STATIC_LIBRARIES += recast_static
LOCAL_WHOLE_STATIC_LIBRARIES += spine_static
LOCAL_WHOLE_STATIC_LIBRARIES += cocos_ui_static
LOCAL_WHOLE_STATIC_LIBRARIES += libvorbisidec

include $(BUILD_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE    := websockets_static
LOCAL_MODULE_FILENAME := libwebsockets_static
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/websockets/prebuilt/android/$(TARGET_ARCH_ABI)/libwebsockets.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/websockets/include/android
LOCAL_CPPFLAGS := -D__STDC_LIMIT_MACROS=1
LOCAL_EXPORT_CPPFLAGS := -D__STDC_LIMIT_MACROS=1

LOCAL_STATIC_LIBRARIES += cocos_ssl_static
LOCAL_STATIC_LIBRARIES += cocos_crypto_static
LOCAL_STATIC_LIBRARIES += ext_uv_static

include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_webp_static
LOCAL_MODULE_FILENAME := webp
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/webp/prebuilt/android/$(TARGET_ARCH_ABI)/libwebp.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/webp/include/android

LOCAL_WHOLE_STATIC_LIBRARIES := cpufeatures_static

ifeq ($(TARGET_ARCH_ABI),armeabi-v7a)
    LOCAL_CFLAGS := -DHAVE_NEON=1
endif

include $(PREBUILT_STATIC_LIBRARY)

$(call import-module,android/cpufeatures)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE    := bullet_static
LOCAL_MODULE_FILENAME := bullet_static
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/bullet/prebuilt/android/$(TARGET_ARCH_ABI)/libLinearMath.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/bullet/include
LOCAL_EXPORT_C_INCLUDES += $(COCOS_ROOT_1)/external/bullet/include/bullet
LOCAL_STATIC_LIBRARIES += cocos_bulletcollision_static
LOCAL_STATIC_LIBRARIES += cocos_bulletdynamics_static
LOCAL_STATIC_LIBRARIES += cocos_bulletmultithreaded_static
# LOCAL_STATIC_LIBRARIES += cocos_linearmath_static
LOCAL_STATIC_LIBRARIES += cocos_minicl_static
include $(PREBUILT_STATIC_LIBRARY)

include $(CLEAR_VARS)
LOCAL_MODULE := cocos_bulletcollision_static
LOCAL_MODULE_FILENAME := bulletcollision
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/bullet/prebuilt/android/$(TARGET_ARCH_ABI)/libBulletCollision.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/bullet/include
LOCAL_STATIC_LIBRARIES += cocos_linearmath_static
include $(PREBUILT_STATIC_LIBRARY)

include $(CLEAR_VARS)
LOCAL_MODULE := cocos_bulletdynamics_static
LOCAL_MODULE_FILENAME := bulletdynamics
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/bullet/prebuilt/android/$(TARGET_ARCH_ABI)/libBulletDynamics.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/bullet/include
LOCAL_STATIC_LIBRARIES += cocos_bulletcollision_static
LOCAL_STATIC_LIBRARIES += cocos_linearmath_static
include $(PREBUILT_STATIC_LIBRARY)

include $(CLEAR_VARS)
LOCAL_MODULE := cocos_bulletmultithreaded_static
LOCAL_MODULE_FILENAME := bulletmultithreaded
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/bullet/prebuilt/android/$(TARGET_ARCH_ABI)/libBulletMultiThreaded.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/bullet/include
include $(PREBUILT_STATIC_LIBRARY)

include $(CLEAR_VARS)
LOCAL_MODULE := cocos_linearmath_static
LOCAL_MODULE_FILENAME := linearmath
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/bullet/prebuilt/android/$(TARGET_ARCH_ABI)/libLinearMath.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/bullet/include
include $(PREBUILT_STATIC_LIBRARY)

include $(CLEAR_VARS)
LOCAL_MODULE := cocos_minicl_static
LOCAL_MODULE_FILENAME := minicl
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/bullet/prebuilt/android/$(TARGET_ARCH_ABI)/libMiniCL.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/bullet/include
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_tiff_static
LOCAL_MODULE_FILENAME := tiff
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/tiff/prebuilt/android/$(TARGET_ARCH_ABI)/libtiff.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/tiff/include/android
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_png_static
LOCAL_MODULE_FILENAME := png
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/png/prebuilt/android/$(TARGET_ARCH_ABI)/libpng.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/png/include/android
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)

LOCAL_MODULE := cocos_crypto_static
LOCAL_MODULE_FILENAME := crypto
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/openssl/prebuilt/android/$(TARGET_ARCH_ABI)/libcrypto.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/openssl/include/android
include $(PREBUILT_STATIC_LIBRARY)

include $(CLEAR_VARS)
LOCAL_MODULE := cocos_ssl_static
LOCAL_MODULE_FILENAME := ssl
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/openssl/prebuilt/android/$(TARGET_ARCH_ABI)/libssl.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/openssl/include/android
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE    := ext_uv_static
LOCAL_MODULE_FILENAME := ext_uv
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/uv/prebuilt/android/$(TARGET_ARCH_ABI)/libuv_a.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/uv/include
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_jpeg_static
LOCAL_MODULE_FILENAME := jpeg
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/jpeg/prebuilt/android/$(TARGET_ARCH_ABI)/libjpeg.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/jpeg/include/android
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_freetype2_static
LOCAL_MODULE_FILENAME := freetype2
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/freetype2/prebuilt/android/$(TARGET_ARCH_ABI)/libfreetype.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/freetype2/include/android           \
                           $(COCOS_ROOT_1)/external/freetype2/include/android/freetype2
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_curl_static
LOCAL_MODULE_FILENAME := curl
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/curl/prebuilt/android/$(TARGET_ARCH_ABI)/libcurl.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/curl/include/android
LOCAL_STATIC_LIBRARIES += cocos_ssl_static
LOCAL_STATIC_LIBRARIES += cocos_crypto_static
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_chipmunk_static
LOCAL_MODULE_FILENAME := chipmunk
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/chipmunk/prebuilt/android/$(TARGET_ARCH_ABI)/libchipmunk.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/chipmunk/include
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)

LOCAL_MODULE    := box2d_static
LOCAL_MODULE_FILENAME := box2d_static
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/Box2D/prebuilt/android/$(TARGET_ARCH_ABI)/libbox2d.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS_ROOT_1)/external/Box2D/include
LOCAL_EXPORT_C_INCLUDES += $(COCOS_ROOT_1)/external/Box2D/include
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_zlib_static
LOCAL_MODULE_FILENAME := zlib
LOCAL_SRC_FILES := $(COCOS_ROOT_1)/external/zlib/prebuilt/android/$(TARGET_ARCH_ABI)/libz.a
LOCAL_EXPORT_C_INCLUDES := $(COCOS)/external/zlib/include
include $(PREBUILT_STATIC_LIBRARY)

#下面是17个构建模块定义，与库需要一一对应
#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_flatbuffers_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/flatbuffers.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := audioengine_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libaudio.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos2dx_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libcc.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos2dxandroid_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libccandroid.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos2dx_internal_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libcc_core.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos3d_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libc3d.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocosbuilder_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libccb.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocosdenshion_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libccds.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocostudio_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libccs.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cpufeatures_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libcpufeatures.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_extension_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libets.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_network_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libnet.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := libpvmp3dec
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libext_pvmp3dec.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := recast_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/librecast.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := spine_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libspine.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := cocos_ui_static
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libui.a
include $(PREBUILT_STATIC_LIBRARY)

#=================================================================================
include $(CLEAR_VARS)
LOCAL_MODULE := libvorbisidec
LOCAL_SRC_FILES := $(TARGET_ARCH_ABI)/libext_vorbisidec.a
include $(PREBUILT_STATIC_LIBRARY)

#==============================================================
