APP_STL := c++_static
APP_PLATFORM := android-9

APP_CPPFLAGS := -frtti -DCC_ENABLE_CHIPMUNK_INTEGRATION=1 -std=c++14 -fsigned-char
APP_LDFLAGS := -latomic
APP_SHORT_COMMANDS := true

ifeq ($(NDK_DEBUG),1)
  APP_CPPFLAGS += -DCOCOS2D_DEBUG=1
  APP_OPTIM := debug
else
  APP_CPPFLAGS += -UNDEBUG
  APP_OPTIM := release
endif
