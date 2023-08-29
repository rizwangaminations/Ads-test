import os, sys
import shutil
import argparse
import json
import filecmp
import fnmatch
import print_utils
import plistlib
import io, re

LOGGER = print_utils.Logger()

def join_path(*args):
    return os.path.normpath(os.path.join(*args))

def key_match(key, patterns_list):
    for pattern in patterns_list:
        if  re.match(pattern, key):
            return pattern
    return ""


def buildDict(dict_key, input_dict, replacement_dict, notifyNotChanged = True):
    output_dict = dict()
    for key in input_dict:
        sub_key = key if dict_key == "" else dict_key + ":" + key
        if isinstance(input_dict[key], dict):
            output_dict[key] = buildDict(sub_key, input_dict[key], replacement_dict, notifyNotChanged)
        elif isinstance(input_dict[key], list):
            output_dict[key] = buildList(sub_key, input_dict[key], replacement_dict, notifyNotChanged)
        else:
            #search for key in replacement_dict that matches current sub_key
            match_replacement_key = key_match(sub_key, list(replacement_dict.keys()))
            if match_replacement_key != "":
                LOGGER.i("Replacing for key %s: (%s -> %s)" % (sub_key, input_dict[key].encode('utf8'), replacement_dict[match_replacement_key].encode('utf8')))
                output_dict[key] = replacement_dict[match_replacement_key]
            else:
                output_dict[key] = input_dict[key]
                if notifyNotChanged == True:
                    LOGGER.w("Key %s remains the same. Not found in replacement dict" % (key))
    return output_dict

def buildList(dict_key, input_list, replacement_dict, notifyNotChanged = True):
    output_list = list()
    for input_list_value in input_list:
        if isinstance(input_list_value, dict):
            output_list.append(buildDict(dict_key, input_list_value, replacement_dict, notifyNotChanged))
        elif isinstance(input_list_value, list):
            output_list.append(buildList(dict_key, input_list_value, replacement_dict, notifyNotChanged))
        #object is not list or dictionary -> it's just buildin type value
        else:
            element_key = dict_key + ":" + str(input_list_value)
            match_replacement_key = key_match(element_key, list(replacement_dict.keys()))
            if match_replacement_key != "":
                LOGGER.i("Replacing for key %s: (%s -> %s)" % (dict_key, input_list_value, replacement_dict[match_replacement_key]))
                output_list.append(replacement_dict[match_replacement_key])
            else:
                output_list.append(input_list_value)
                if notifyNotChanged == True:
                    LOGGER.w("Key %s remains the same. Not found in replacement dict" % (key))
    return output_list

def updatePlist(input_plist, newData, notifyNotChanged = True):
    with open(input_plist, 'rb') as fp:
        plistData = plistlib.load(fp)
    output_dict = buildDict("", plistData, newData, notifyNotChanged)
    with open(input_plist, 'wb') as fp:
        plistlib.dump(output_dict, fp)

def replaceInFile(file_path, replacement_map):
    with open(file_path, 'r') as manifest_file:
        new_file = io.open(file_path + "._tmp", mode='w', newline='\n')
        for line in manifest_file:
            for source, dist in replacement_map.items():
                line = re.sub(source, dist, line)
            if type(line) == str:
                line_to_write = line
            elif type(line) == str:
                line_to_write = line
            new_file.write(line_to_write)
        new_file.close()
    os.remove(file_path)
    os.rename(file_path + "._tmp", file_path)

def stringify(input):
    if type(input) == float:
        return str(int(input))
    else:
        return input

if __name__ == '__main__':
    LOGGER.h("Installing XLRD python library...")
    try:
        os.system("python -m pip install xlrd==1.2.0")
        import xlrd
        LOGGER.i("Python XLRD INSTALLED", 4)
    except:
        LOGGER.w("Failed to install XLRD python library")
        exit(0)
    print((60 * '-'))

    parsed_keys = {
        "ios" : {},
        "android" : {},
        "amazon" : {},
        "windows_phone" : {}
    }

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--xlsx_file', type=str, default="keys.xlsx", help="Input xlsx config file")
    arg_parser.add_argument('-d', '--dir', type=str, default="MiniGameData", help="working MiniGameData directory")
    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    xlsx_full_path = join_path(script_dir, args.xlsx_file)
    output_root_dir = join_path(script_dir, args.dir)

    LOGGER.h("Parsing %s file" % xlsx_full_path)
    rb = xlrd.open_workbook(xlsx_full_path)
    sheet = rb.sheet_by_index(0)
    for rowIdx in range(1, sheet.nrows):
        row = sheet.row(rowIdx)
        description = stringify(row[0].value)
        keys = stringify(row[2].value)
        if keys == "-" or keys == "":
            continue
        for key in keys.split(";"):
            parsed_keys["ios"][key] = stringify(row[3].value)
            parsed_keys["android"][key] = stringify(row[4].value)
            parsed_keys["amazon"][key] = stringify(row[5].value)
            parsed_keys["windows_phone"][key] = stringify(row[6].value)

    #update Amazon API KEY UPDATE

    apikey_file_path = join_path(output_root_dir, "Amazon/api_key.txt")
    os.remove(apikey_file_path)
    new_file = io.open(apikey_file_path , mode='w', newline='\n')
    new_file.write(parsed_keys["amazon"]["API_KEY"])
    new_file.close()

    #update AddOneSignalKey

    keysPlistPath = join_path(output_root_dir, "Data/sdkkeys.plist")
    if os.path.isfile(keysPlistPath):
        os.remove(keysPlistPath)
    new_file = io.open(keysPlistPath , mode='w', newline='\n')
    new_file.close()
    output_dict = {
            "onesignalKey" : parsed_keys["android"]["ONE_SIGNAL_KEY"],
            "GADApplicationIdentifier" : parsed_keys["ios"]["ADMOB_APP_ID"]
    }
    with open(keysPlistPath, 'wb') as fp:
        plistlib.dump(output_dict, fp)


    #update iOS/Android/Amazon/WP8.1 plists
    configs_map = {
        "ios" : "Resources/Misc/data/ios/Configurations.plist",
        "android" : "Resources/Misc/data/android/Configurations.plist"
    }
    for platform, config_file in configs_map.items():
        LOGGER.h("%s: updating %s" % (platform, config_file))
        config_full_path = join_path(output_root_dir, config_file)
        updatePlist(config_full_path, parsed_keys[platform])
        print((70 * '-'))


    #Update/Users/admin/Job/projects/Freelance/GameRoot/proj.ios_mac/ios/Info.plist Android/Amazon XMLs
    for platform in ["android", "amazon"]:
        #Update AndroidManifest.xml
        manifest_file = join_path(output_root_dir, "%s/AndroidManifest.xml" % platform)
        manifest_replacements = {
            'package=".*?"' : 'package="%s"' % parsed_keys[platform]["PACKAGE_NAME"],
            'android:versionName=".*?"' : 'android:versionName="%s"' % parsed_keys[platform]["APP_VERSION"],
            'android:versionCode=".*?"' : 'android:versionCode="%s"' % parsed_keys[platform]["BUILD_NUMBER"],
            'android:authorities="com.facebook.app.FacebookContentProvider.*?"' : 'android:authorities="com.facebook.app.FacebookContentProvider%s"' % parsed_keys[platform]["FACEBOOK_APP_ID"]
        }
        LOGGER.h("%s: updating %s file" % (platform, manifest_file))
        replaceInFile(manifest_file, manifest_replacements)

        #Update res/values/strings.xml
        strings_file = join_path(output_root_dir, "%s/res/values/strings.xml" % platform)
        strings_replacement_map = {
            '<string name="app_name">.*?</string>' : '<string name="app_name">%s</string>' % parsed_keys[platform]["APP_NAME"],
            '<string name="firebase_sender_id">.*?</string>' : '<string name="firebase_sender_id">%s</string>' % parsed_keys[platform]["firebase_sender_id"],
            '<string name="firebase_application_id">.*?</string>' : '<string name="firebase_application_id">%s</string>' % parsed_keys[platform]["firebase_application_id"],
            '<string name="facebook_app_id">.*?</string>' : '<string name="facebook_app_id">%s</string>' % parsed_keys[platform]["FACEBOOK_APP_ID"],
            '<string name="facebook_client_token">.*?</string>' : '<string name="facebook_client_token">%s</string>' % parsed_keys[platform]["FACEBOOK_CLIENT_TOKEN"],
            '<string name="branch_key_live">.*?</string>' : '<string name="branch_key_live">%s</string>' % parsed_keys[platform]["BRANCH_KEY_LIVE"],
            '<string name="branch_key_test">.*?</string>' : '<string name="branch_key_test">%s</string>' % parsed_keys[platform]["BRANCH_KEY_TEST"],
            '<string name="branch_uri_scheme">.*?</string>' : '<string name="branch_uri_scheme">%s</string>' % parsed_keys[platform]["URL_SCHEME"],
            '<string name="branch_uri_domain">.*?</string>' : '<string name="branch_uri_domain">%s</string>' % parsed_keys[platform]["APP_LINK"],
            '<string name="branch_uri_alt_domain">.*?</string>' : '<string name="branch_uri_alt_domain">%s</string>' % parsed_keys[platform]["APP_ALTERNATE_LINK"],
            '<string name="ADMob_Key">.*?</string>' : '<string name="ADMob_Key">%s</string>' % parsed_keys[platform]["ADMOB_APP_ID"],
            '<string name="fcm_project_id">.*?</string>' : '<string name="fcm_project_id">%s</string>' % parsed_keys[platform]["FCM_PROJECT_ID"],
            '<string name="fcm_api_key">.*?</string>' : '<string name="fcm_api_key">%s</string>' % parsed_keys[platform]["FCM_API_KEY"]
        }
        LOGGER.h("%s: updating %s file" % (platform, strings_file))
        replaceInFile(strings_file, strings_replacement_map)


    #Update ios xcconfig
    ios_xcconfig_file = join_path(output_root_dir, "ios/Config_ios.xcconfig")
    ios_xcconfig_replacements = {
        'PRODUCT_BUNDLE_IDENTIFIER = .*$' : 'PRODUCT_BUNDLE_IDENTIFIER = %s' % parsed_keys["ios"]["PRODUCT_BUNDLE_IDENTIFIER"],
        'PRODUCT_NAME = .*$' : 'PRODUCT_NAME = %s' % parsed_keys["ios"]["PRODUCT_NAME"],
        'FABRIC_APIKEY = .*$' : 'FABRIC_APIKEY = %s' % parsed_keys["ios"]["FABRIC_API_KEY"],
        'FABRIC_API_SECRET = .*$' : 'FABRIC_API_SECRET = %s' % parsed_keys["ios"]["FABRIC_API_SECRET"]
    }
    LOGGER.h("ios: updating %s file" % (ios_xcconfig_file))
    replaceInFile(ios_xcconfig_file, ios_xcconfig_replacements)
    #Update ios Info.plist file
    ios_plist_file = join_path(output_root_dir, "ios/Info.plist")
    ios_plist_replacements = {
        'CFBundleDisplayName' : parsed_keys["ios"]["APP_NAME"],
        'CFBundleName' : parsed_keys["ios"]["APP_BUNDLE_NAME"],        
        'CFBundleShortVersionString' : parsed_keys["ios"]["APP_VERSION"],
        'CFBundleVersion' : parsed_keys["ios"]["BUILD_NUMBER"],
        'FacebookAppID' : parsed_keys["ios"]["FACEBOOK_APP_ID"],
        'FacebookClientToken' : parsed_keys["ios"]["FACEBOOK_CLIENT_TOKEN"],
        'FacebookDisplayName' : parsed_keys["ios"]["APP_NAME"],
        'Fabric:APIKey' : parsed_keys["ios"]["FABRIC_API_KEY"],
        'CFBundleURLTypes:CFBundleURLSchemes:fb*' : "fb%s" % parsed_keys["ios"]["FACEBOOK_APP_ID"],
        'branch_key:live' : parsed_keys["ios"]["BRANCH_KEY_LIVE"],
        'branch_key:test' : parsed_keys["ios"]["BRANCH_KEY_TEST"],
        'NSUserTrackingUsageDescription' : parsed_keys["ios"]["ATT_POPUP_DESCRIPTION"]
    }
    LOGGER.h("ios: updating %s file" % (ios_plist_file))
    updatePlist(ios_plist_file, ios_plist_replacements, False)
    
    #Update ios Info.plist for URLSchemes
    with open(ios_plist_file, 'rb') as fp:
        ios_plist_data = plistlib.load(fp)
    plist_url_arr = ios_plist_data["CFBundleURLTypes"]
    for array_item in plist_url_arr:
        url_schemes = [x.strip() for x in parsed_keys["ios"]["URL_SCHEME"].split(',')]
        array_item["CFBundleURLSchemes"] = url_schemes
    with open(ios_plist_file, 'wb') as fp:
        plistlib.dump(ios_plist_data, fp)
    
    ios_entitlement_file = join_path(output_root_dir, "ios/SlotGame-mobile.entitlements")
    with open(ios_entitlement_file, 'rb') as fp:
        ios_entitlement_data = plistlib.load(fp)
    app_links = list()
    app_links.append(parsed_keys["ios"]["APP_LINK"])
    app_links.append(parsed_keys["ios"]["APP_ALTERNATE_LINK"])
    ios_entitlement_data["com.apple.developer.associated-domains"] = app_links
    ios_entitlement_data["com.apple.developer.icloud-container-identifiers"] = [parsed_keys["ios"]["ICLOUD_IDENTIFIER"]]
    ios_entitlement_data["com.apple.developer.ubiquity-container-identifiers"] = [parsed_keys["ios"]["ICLOUD_IDENTIFIER"]]
    with open(ios_entitlement_file, 'wb') as fp:
        plistlib.dump(ios_entitlement_data, fp)
    
    #update WP8.1 Package.manifest
    wp81_manifest_file = join_path(output_root_dir, "Windows/Package.appxmanifest")
    wp81_manifest_replacements = {
        '<DisplayName>.*?</DisplayName>' : '<DisplayName>%s</DisplayName>' % parsed_keys["windows_phone"]["APP_NAME"],
        ' Version=".*?"' : ' Version="%s.0"' % parsed_keys["windows_phone"]["APP_VERSION"]
    }
    LOGGER.h("windows_phone: updating manifest %s" % (wp81_manifest_file))
    replaceInFile(wp81_manifest_file, wp81_manifest_replacements)
