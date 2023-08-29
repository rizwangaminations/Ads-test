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



def applyKeys():
    keysPlistPath = join_path(output_root_dir, "Data/sdkkeys.plist")
    with open(keysPlistPath, 'rb') as fp:
        plistData = plistlib.load(fp)
    onesignalKey = plistData["onesignalKey"]
    GADApplicationIdentifierKey = plistData["GADApplicationIdentifier"]

    gradle_file = join_path(script_dir, "../proj.android-as/build.gradle")
    gradle_replacement_map = {
        'onesignal_app_id = ".*?"' : 'onesignal_app_id = "%s"' % onesignalKey

    }
    replaceInFile(gradle_file, gradle_replacement_map)

    gradle_file = join_path(script_dir, "../proj.amazon-as/build.gradle")
    gradle_replacement_map = {
        'onesignal_app_id = ".*?"' : 'onesignal_app_id = "%s"' % onesignalKey
        }
    replaceInFile(gradle_file, gradle_replacement_map)
    
    string_rename_replacements = {
        '#define GADApplicationIdentifier @\(\(".*?"\)\)' : '#define GADApplicationIdentifier @(("%s"))' % GADApplicationIdentifierKey
    }
    string_rename_file_path = join_path(script_dir, "../proj.ios_mac/ios/NSBundle+NSBundle.mm")
    replaceInFile(string_rename_file_path, string_rename_replacements)





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


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--dir', type=str, default="MiniGameData", help="working MiniGameData directory")
    args = arg_parser.parse_args()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_root_dir = join_path(script_dir, args.dir)

    applyKeys()



