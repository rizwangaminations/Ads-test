//
//  CommonModuleConstants.h
//  Common1
//
//  Created by Muhammad Arslan on 12/08/2015.
//
//

#ifndef Common1_CommonModuleConstants_h
#define Common1_CommonModuleConstants_h

#include <functional>
#include <string>

enum class Currency : char
{
    COINS, GEMS
};

class Reward
{
private:
    Currency  m_currency;
    long long m_value;
    
public:
    Reward(Currency currency, long long value)
    : m_currency(currency)
    , m_value(value)
    { };
    
    inline Currency  getCurrency() const { return m_currency; };
    inline long long getValue()    const { return m_value; };
    
    inline std::string getRewardType() const
    {
        if (m_currency == Currency::COINS) return ("GRIND");
        if (m_currency == Currency::GEMS)  return ("PREMIUM_GRIND");
        return ("DEFAULT");
    };
    
    inline std::string getCurrencyName() const
    {
        if (m_currency == Currency::COINS) return ("COINS");
        if (m_currency == Currency::GEMS)  return ("GEMS");
        return ("DEFAULT");
    };
};

#define GAME_COMMON_INSTALL_TIME ("GAME_COMMON_INSTALL_TIME")

#define MODULE_COMMON_SETTINGS_LOADED_EVENT ("MODULE_COMMON_SETTINGS_LOADED_EVENT")
#define DISABLE_BUTTON_COLOR Color3B(192,192,192)
    
#define SOUND_SETTING_CHANGED_EVENT ("SOUND_SETTING_CHANGED_EVENT")
#define LEVEL_BUTTON_DOWNLOADED_EVENT ("LEVEL_BUTTON_DOWNLOADED_EVENT")
#define MANAGED_BACKGROUND_TASK_STARTED ("MANAGED_BACKGROUND_TASK_STARTED")
#define RELEASE_CACHED_RESOURCES ("RELEASE_CACHED_RESOURCES")
#define DEFAULT_BUTTON_SIZE cocos2d::Size(500, 430)
#define OPEN_LOADING_SCENE_FOR_LEVEL ("OPEN_LOADING_SCENE_FOR_LEVEL")

#endif
