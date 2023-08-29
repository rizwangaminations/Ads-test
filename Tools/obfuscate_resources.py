import os, sys
import shutil
import argparse
import json
import filecmp
import fnmatch
import zipfile
import random
import string
import fileinput
import plistlib
import io, re
import hashlib
from shutil import move
from tempfile import mkstemp
from os import fdopen, remove


hashed_string = {}
private_key = ""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(color, message):
    print(color + message + bcolors.ENDC)

def print_warning(message):
    print_colored(bcolors.WARNING, "WARNING: " + message)

def print_error(message):
    print_colored(bcolors.FAIL, "ERROR: " + message)

def print_info(message):
    print_colored(bcolors.OKBLUE, "INFO: " + message)


def join_path(*arg):
    return os.path.normpath(os.path.join(*arg))

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

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
                output_dict[key] = replacement_dict[match_replacement_key]
            else:
                output_dict[key] = input_dict[key]
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
                output_list.append(replacement_dict[match_replacement_key])
            else:
                output_list.append(input_list_value)
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
            for source, dist in list(replacement_map.items()):
                line = re.sub(source, dist, line)
            if type(line) == str:
                line_to_write = line
            elif type(line) == str:
                line_to_write = line
            new_file.write(line_to_write)
        new_file.close()
    os.remove(file_path)
    os.rename(file_path + "._tmp", file_path)

def getValueForKeyFromXcodeConfigFile(file_path, key):
    file = open(file_path, "r")
    read = file.read()

    for line in read.splitlines():
        if key in line:
            return line.split('=',1)[1].strip()

def renameFile(old_file_path, new_file_path):
    os.rename(old_file_path, new_file_path)

def getEncryptedName(file_name):
    if file_name in hashed_string:
        return hashed_string[file_name]
    
    to_encrypt_file_name = file_name + private_key
    encript1 = hashlib.md5(to_encrypt_file_name.encode())
    encrypted_string = encript1.hexdigest()
    hashed_string[file_name] = encrypted_string
    return encript1.hexdigest()

def getObfuscatedName(full_file_name):
    if os.path.isdir(full_file_name):
        head, tail = os.path.split(full_file_name)
        return getEncryptedName(tail.strip("/"))

    else:
        file_name = getFileNameFromPath(full_file_name)
        file_extention = getFileExtentionFromPath(full_file_name)
        new_file_name = getEncryptedName(file_name) + file_extention
        return new_file_name

def obfuscateFile(full_file_path, obfuscated_name):
    full_new_file_path = join_path(os.path.dirname(full_file_path), obfuscated_name)
    renameFile(full_file_path, full_new_file_path)

def obfuscateDirectory(full_directory_path, obfuscated_name):
    if os.path.isdir(full_directory_path):
        head, tail = os.path.split(full_directory_path)
        full_new_directory_path = join_path(head, obfuscated_name)
        renameFile(full_directory_path, full_new_directory_path)

def getFullFileNameFromPath(full_file_path):
    return os.path.basename(full_file_path)

def getFileNameFromPath(full_file_path):
    return os.path.splitext(os.path.basename(full_file_path))[0]

def getFileExtentionFromPath(full_file_path):
    return os.path.splitext(os.path.basename(full_file_path))[1]

def getImmediateSubdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def obfuscateDirectoryContent(dir_path):
    all_directories = []
    for r, d, f in os.walk(dir_path):
        for directory in d:
            full_directory_path = os.path.join(r, directory)
            all_directories.append(full_directory_path)

    for rr, dd, ff in os.walk(dir_path):
        for file in ff:
            full_file_path = os.path.join(rr, file)
#            print_info("File:" + full_file_path)
            if not file.endswith('.DS_Store'):
                obfuscated_file_name = getObfuscatedName(full_file_path)
                obfuscateFile(full_file_path, obfuscated_file_name)

    for i in range(len(all_directories),0,-1):
        full_directory_path = all_directories[i-1]
        obfuscated_directory_name = getObfuscatedName(full_directory_path)
        obfuscateDirectory(full_directory_path, obfuscated_directory_name)

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
 
 # Start Resource Folders renaming
    xcode_config_path = join_path(dir_path, "../proj.ios_mac/ios/Config_ios.xcconfig")
    private_key = getValueForKeyFromXcodeConfigFile(xcode_config_path, "PRODUCT_BUNDLE_IDENTIFIER")
    file_utils_replacements = {
        '#define PROJECT_KEY ".*?"' : '#define PROJECT_KEY "%s"' % private_key
    }
    file_utils_file_path = join_path(dir_path, "../Classes/AppDelegate.cpp")
    replaceInFile(file_utils_file_path, file_utils_replacements)

    string_rename_replacements = {
        'constexpr char PROJECT_KEY\[\] = ".*?";' : 'constexpr char PROJECT_KEY[] = "%s";' % private_key
    }
    string_rename_file_path = join_path(dir_path, "../modulecommon/StringRename.h")
    replaceInFile(string_rename_file_path, string_rename_replacements)
    
    obfuscate_directories = []
    obfuscate_directories.append('../Resources/Common')
    obfuscate_directories.append('../Resources/Content')
    obfuscate_directories.append('../Resources/ios')
    obfuscate_directories.append('../Resources/android')

    ios_project_file_replacements = {}
    
    for directory in obfuscate_directories:
        full_directory_path = join_path(dir_path, directory)
        immediateSubdirectories = getImmediateSubdirectories(full_directory_path)
        obfuscateDirectoryContent(full_directory_path)
        
        for directory in immediateSubdirectories:
            full_directory_path = os.path.join(full_directory_path, directory)
            obfuscated_directory_name = getObfuscatedName(full_directory_path)
            ios_project_file_replacements[" " + directory.strip("/") + " "] = " " + obfuscated_directory_name.strip("/") + " "
            ios_project_file_replacements[directory.strip("/") + ";"] = obfuscated_directory_name.strip("/") + ";"

    ios_project_file_path = join_path(dir_path, "../proj.ios_mac/SlotGame.xcodeproj/project.pbxproj")
    replaceInFile(ios_project_file_path, ios_project_file_replacements)

# End Resource Folders renaming

    proj_ios_path = join_path(dir_path, "../proj.ios_mac/SlotGame-mobile/Images.xcassets")
    proj_ios_launchscreens_path = join_path(dir_path, "../proj.ios_mac/SlotGame-mobile")

    if not os.path.exists(proj_ios_path):
        print_error("Path doesn't exists..  skipping..")
        sys.exit(1)

    ios_project_temp_file_path = join_path(dir_path, "../proj.ios_mac/SlotGame.xcodeproj/projectTemp.pbxproj")
    appicon_search_expression = "ASSETCATALOG_COMPILER_APPICON_NAME"
    launchscreen_search_expression = ".storyboard"

    product_name = getValueForKeyFromXcodeConfigFile(xcode_config_path, "PRODUCT_NAME")
    random_appicon_name = product_name
    random_launchscreen_name = product_name

# Renaming AppIcons Folder
    for r, d, f in os.walk(proj_ios_path):
        for directory in d:
            full_directory_path = os.path.join(r, directory)
            final_icon_name = random_appicon_name + ".appiconset"
            full_new_directory_path = os.path.join(r, final_icon_name)
            os.rename(full_directory_path, full_new_directory_path)
            break;
# Renaming LaunchScreen
    for r, d, f in os.walk(proj_ios_launchscreens_path):
        for file in f:
            if (file.find(launchscreen_search_expression) != -1):
                final_launchscreen_name = random_launchscreen_name + ".storyboard"
                current_launchscreen_path = os.path.join(proj_ios_launchscreens_path, file)
                full_new_launchscreen_path = os.path.join(proj_ios_launchscreens_path, final_launchscreen_name)
                os.rename(current_launchscreen_path, full_new_launchscreen_path)

# Editing Info.plist file for Launch Screen name changes
    ios_plist_file = join_path(dir_path, "../proj.ios_mac/ios/Info.plist")
    ios_plist_replacements = {
        'UILaunchStoryboardName' : random_launchscreen_name
    }
    updatePlist(ios_plist_file, ios_plist_replacements, False)

# Editing Project file for AppIcon and LAunchScreen Changes
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(ios_project_file_path) as old_file:
            for line in old_file:
                if (line.find(appicon_search_expression) != -1):
                    new_file.write(appicon_search_expression + " = " + random_appicon_name + ";")
                elif (line.find(launchscreen_search_expression) != -1):
                    final_line = ""
                    splitted_words = line.split()
                    for single_word in splitted_words:
                        if (single_word.find(launchscreen_search_expression) != -1 and single_word != "file.storyboard;"):
                            word_to_replace = os.path.basename(os.path.normpath(single_word.split(".")[0]))
                            final_line = final_line + " " + single_word.replace(word_to_replace, random_launchscreen_name)
                        else:
                            final_line = final_line + " " + single_word

                    final_line = final_line + "\n"
                    new_file.write(final_line)
                else:
                    new_file.write(line)
    remove(ios_project_file_path)
    move(abs_path, ios_project_file_path)
