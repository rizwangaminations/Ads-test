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



def applyProjectProperties():
    propertiesPlistPath = join_path(output_root_dir, "Data/ProjectProperties.plist")
    if os.path.exists(propertiesPlistPath):
        with open(propertiesPlistPath, 'rb') as fp:
            plistData = plistlib.load(fp)
        is_admob_enabled = plistData["IS_ADMOB_ENABLED"]

        gradle_file = join_path(script_dir, "../proj.android-as/gradle.properties")
        gradle_replacement_map = {
            'IS_ADMOB_ENABLED=.*?e' : 'IS_ADMOB_ENABLED=%s' % is_admob_enabled
        }
        replaceInFile(gradle_file, gradle_replacement_map)



def replaceInFile(file_path, replacement_map):
    with open(file_path, 'r') as manifest_file:
        new_file = io.open(file_path + "._tmp", mode='w', newline='\n')
        for line in manifest_file:
            for source, dist in replacement_map.items():
                line = re.sub(source, dist, line)
            if type(line) == str:
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

    applyProjectProperties()



