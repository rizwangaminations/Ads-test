import os, sys
import shutil
import plistlib
import io, re

def join_path(*args):
    return os.path.normpath(os.path.join(*args))


def get_bonus_game_id(bonus_game_key, config_file):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    settings_plist_path = join_path(script_dir, config_file)
    with open(settings_plist_path, 'rb') as fp:
        plistData = plistlib.readPlist(fp)
    if plistData['results'][0].get(bonus_game_key, None):
        return plistData['results'][0][bonus_game_key]
    return ""

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    bonus_game_plist_path = join_path(script_dir, "../Resources/Common/ModuleBonusGameResources/bonusGames/BonusGames.plist")
    mainmenu_bonus_game_old_path = join_path(script_dir, "../Resources/Common/ModuleBonusGameResources/bonusGames/BonusGame_local")
    if os.path.isdir(mainmenu_bonus_game_old_path):
        mainmenu_bonus_game_key = get_bonus_game_id('MainMenuBonusGameId', "../Resources/Misc/Configs/Settings.plist")
        if mainmenu_bonus_game_key != "":
            mainmenu_bonus_game_new_path = join_path(script_dir, "../Resources/Common/ModuleBonusGameResources/bonusGames/BonusGame_" + mainmenu_bonus_game_key)
            os.rename(mainmenu_bonus_game_old_path, mainmenu_bonus_game_new_path)
            with open(bonus_game_plist_path, 'rb') as fp:
                 bonus_plist = plistlib.readPlist(fp)
            for it in bonus_plist['results']:
                if it.objectId == 'local':
                    it.objectId = mainmenu_bonus_game_key
                    break
            plistlib.writePlist(bonus_plist, bonus_game_plist_path)
    daily_bonus_game_old_path = join_path(script_dir, "../Resources/Common/ModuleBonusGameResources/bonusGames/BonusGame_dailybonus")
    if os.path.isdir(daily_bonus_game_old_path):
        daily_bonus_game_key = get_bonus_game_id('DailyBonusGameId', "../Resources/Misc/Configs/Settings.plist")
        if daily_bonus_game_key != "":
            daily_bonus_game_new_path = join_path(script_dir, "../Resources/Common/ModuleBonusGameResources/bonusGames/BonusGame_" + daily_bonus_game_key)
            os.rename(daily_bonus_game_old_path, daily_bonus_game_new_path)
            bonus_game_plist_path = join_path(script_dir, "../Resources/Common/ModuleBonusGameResources/bonusGames/BonusGames.plist")
            with open(bonus_game_plist_path, 'rb') as fp:
                bonus_plist = plistlib.readPlist(fp)
            for it in bonus_plist['results']:
                if it.objectId == 'dailybonus':
                    it.objectId = daily_bonus_game_key
                    break
            plistlib.writePlist(bonus_plist, bonus_game_plist_path)
    router_bonus_game_old_path = join_path(script_dir, "../Resources/Common/ModuleBonusGameResources/bonusGames/BonusGame_mainrouter")
    if os.path.isdir(router_bonus_game_old_path):
        router_bonus_game_key = get_bonus_game_id('BonusGameRouterID', "../Resources/Misc/Configs/Worlds.plist")
        if router_bonus_game_key != "":
            router_bonus_game_new_path = join_path(script_dir, "../Resources/Common/ModuleBonusGameResources/bonusGames/BonusGame_" + router_bonus_game_key)
            os.rename(router_bonus_game_old_path, router_bonus_game_new_path)
            bonus_game_plist_path = join_path(script_dir, "../Resources/Common/ModuleBonusGameResources/bonusGames/BonusGames.plist")
            with open(bonus_game_plist_path, 'rb') as fp:
                bonus_plist = plistlib.readPlist(fp)
                for it in bonus_plist['results']:
                    if it.objectId == 'mainrouter':
                        it.objectId = router_bonus_game_key
                        break
            plistlib.writePlist(bonus_plist, bonus_game_plist_path)
