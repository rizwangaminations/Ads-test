import os
import json, http.client, requests
import argparse
import print_utils
import custom_plistlib
import common_utils
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import zipfile
import shutil

LOGGER = print_utils.Logger()


def fix_Nulls(input_data):
    if isinstance(input_data, dict):
        output_data = dict()
        for key in list(input_data.keys()):
            if input_data[key] is None:
                output_data[key] = ""
            else:
                output_data[key] = fix_Nulls(input_data[key])
    elif isinstance(input_data, list):
        output_data = list()
        for val in input_data:
            if val is None:
                output_data.append("")
            else:
                output_data.append(fix_Nulls(val))
    else:
        output_data = input_data
    return output_data


def download_bonusgames(data, download_file_path):
    for bonusGame in data["results"]:
        download_bonusgame(bonusGame, download_file_path)


def download_bonusgame(bonusGame, download_file_path):
    bonusgame_folder = "BonusGame_" + bonusGame["objectId"]
    bonusgame_folder_path = download_file_path + bonusgame_folder + "/"
    version_folder_path = bonusgame_folder_path + "v" + str(bonusGame["version"]) + "/"
    gfx_folder_path = version_folder_path + "gfx/"
    sd_assets_path = gfx_folder_path + "SD/"
    hd_assets_path = gfx_folder_path + "HD/"
    hdr_assets_path = gfx_folder_path + "HDR/"
    ios_path = version_folder_path + "ios/"
    android_path = version_folder_path + "android/"
    ios_sfx_path = ios_path + "sfx/"
    android_sfx_path = android_path + "sfx/"
    try:
        os.mkdir(bonusgame_folder_path)
        os.mkdir(version_folder_path)
        os.mkdir(gfx_folder_path)
        os.mkdir(ios_path)
        os.mkdir(android_path)
        os.mkdir(sd_assets_path)
        os.mkdir(hd_assets_path)
        os.mkdir(hdr_assets_path)
        os.mkdir(ios_sfx_path)
        os.mkdir(android_sfx_path)
    except OSError:
        LOGGER.e("Failed to create a required directory")
    LOGGER.h("|-- Downloading %s --|" % bonusGame["objectId"])
    download_and_unzip_file(bonusGame, "BonusBundle_Common", version_folder_path)
    download_and_unzip_file(bonusGame, "BonusBundle_HD", hd_assets_path)
    download_and_unzip_file(bonusGame, "BonusBundle_HDR", hdr_assets_path)
    download_and_unzip_file(bonusGame, "BonusBundle_SD", sd_assets_path)
    download_and_unzip_file(bonusGame, "Bonus_sfx_android", android_sfx_path)
    download_and_unzip_file(bonusGame, "Bonus_sfx_ios", ios_sfx_path)


def download_and_unzip_file(bonusGame, name, folder):
    if name in bonusGame:
        file_url = bonusGame[name]["url"]
        file_name = bonusGame[name]["name"]
        file_path = folder + file_name
        download_successful = download_file(file_path, file_url)
        if download_successful:
            zip_ref = zipfile.ZipFile(file_path, 'r')
            zip_ref.extractall(folder)
            zip_ref.close()
            os.remove(file_path)
            macosx_folder_path = folder + "__MACOSX"
            if os.path.isdir(macosx_folder_path):
                shutil.rmtree(macosx_folder_path)


def download_file(file_path, file_url):
    retries = 3
    download_successful = True
    request = urllib.request.urlopen(file_url, timeout=30)
    with open(file_path, 'wb') as f:
        try:
            f.write(request.read())
        except:
            if retries > 0:
                LOGGER.w("Failed download, retrying...")
                retries -= 1
                download_file(file_path, file_url)
            else:
                LOGGER.e("Request timed out, skipped file %s from bonusgame %s" % (name, bonusGame["objectId"]))
                download_successful = False
    return download_successful


class ParseEntity:
    def __init__(self, app_id, api_key, class_name, dest_path, comment, shouldSyncBonusGames):
        self.app_id = app_id
        self.api_key = api_key
        self.dest_path = dest_path
        self.class_name = class_name
        self.comment = comment
        self.shouldSyncBonusGames = shouldSyncBonusGames

    def sync(self, parse_url):
        LOGGER.i("Sync class '%s' with '%s' (%s)" % (parse_entity.class_name, parse_entity.dest_path, self.comment))
        url = "%s/classes/%s" % (parse_url, self.class_name)
        params = {'limit': 500}
        headers = {
            "Content-Type": "application/json",
            "X-Parse-Application-Id": self.app_id,
            "X-Parse-REST-API-Key": self.api_key
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code >= 200 and response.status_code <= 300:
            result = json.loads(response.text)
            fixed_result = fix_Nulls(result)
            if self.class_name == "BonusGames" and self.shouldSyncBonusGames == "true":
                download_file_path = self.dest_path.rsplit('/', 1)[0] + "/"
                download_bonusgames(fixed_result, download_file_path)
            try:
                with open(self.dest_path, "w") as plist_file:
                    custom_plistlib.writePlist(fixed_result, plist_file)
            except Exception as e:
                LOGGER.e("'%s'  -> '%s': (%s)" % (self.class_name, self.dest_path, str(e)), 4)
        else:
            LOGGER.e("Failed to perform response (%s): %d - %s" % (url, response.status_code, response.text))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-j', '--json', type=str, default="sync_parse_config.json",
                            help="Input json file with Parse sync configuration")
    arg_parser.add_argument('-sb', '--syncBonusGames', type=str, default="true",
                            help="Should Sync BonusGames")

    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_full_path = common_utils.join_path(script_dir, args.json)
    shouldSyncBonusGames = args.syncBonusGames

    LOGGER.i("Loading configuration data from %s" % (json_full_path))
    with open(json_full_path) as config_file:
        config_data = json.load(config_file)
    parse_url = config_data["parse_url"]
    parse_app_id = config_data["parse_app_id"]
    parse_api_key = config_data["parse_api_key"]
    LOGGER.h("Parse URL: %s" % parse_url)
    LOGGER.h("Parse App ID: %s" % parse_app_id)
    LOGGER.h("Parse API Key: %s" % parse_api_key)


    parse_entities = []
    for table in config_data["tables"]:
        class_name = table["class"]
        json_dir = os.path.dirname(json_full_path)
        dest_path = common_utils.join_path(json_dir, table["file_path"])
        comment = table["comment"] if "comment" in table else ""
        parse_entity = ParseEntity(parse_app_id, parse_api_key, class_name, dest_path, comment, shouldSyncBonusGames)
        parse_entities.append(parse_entity)

    for parse_entity in parse_entities:
        parse_entity.sync(parse_url)
