import os, sys
import shutil
import argparse
import json
import filecmp
import fnmatch
import zipfile


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

def zipdir(path, ziphandler):
    # ziphandler is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziphandler.write(os.path.join(root, file))

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-j', '--json_config', type=str, help="Input json config file")
    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_json_full_path = join_path(script_dir, args.json_config)
    
    if not os.path.exists(source_json_full_path):
        print_error("Zip Config not found..  skipping..")
        sys.exit(1)
    
    with open(source_json_full_path) as source_config_file:
        source_data = json.load(source_config_file)

    if "zip_directories" in source_data:
        zip_directories = source_data["zip_directories"]
        for zip_data in zip_directories:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            source_path = join_path(script_dir, zip_data["source"])
            output_file = join_path(script_dir, zip_data["output"])
            print_info("Producing: " + output_file)
            
            file_extension = "zip"
            
            shutil.make_archive(output_file, file_extension, source_path)
            shutil.rmtree(source_path)
            os.rename(output_file + "." + file_extension, output_file)

