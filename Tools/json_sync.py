import os, sys
import shutil
import argparse
import json
import filecmp
import fnmatch

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

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-j', '--json_config', type=str, help="Input json config file")
    arg_parser.add_argument('-d', '--destination', type=str, help="Input destination config file")
    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    source_json_full_path = join_path(script_dir, args.json_config)
    destination_json_full_path = join_path(script_dir, args.destination)
    
    if not os.path.exists(source_json_full_path):
        print_error("Source ResourcePreloadingData.json Not found Under Skin. Skipping ")
        sys.exit(1)
    if not os.path.exists(destination_json_full_path):
        print_error("Destination ResourcePreloadingData.json Not found Under MiniGameData. Skipping ")
        sys.exit(1)

    with open(source_json_full_path) as source_config_file:
        source_data = json.load(source_config_file)
        
    with open(destination_json_full_path) as destination_config_file:
        destination_data = json.load(destination_config_file)

    didModifyDestinationData = None
    if "remove" in source_data:
        removeData = source_data["remove"]
        for key in list(removeData.keys()):
            if key not in destination_data:
                continue
            for removeRow in removeData[key]:
                for destRow in destination_data[key]:
                    if destRow == removeRow:
                        destination_data[key].remove(destRow)
                        didModifyDestinationData = True

    if "add" in source_data:
        addData = source_data["add"]
        for key in list(addData.keys()):
            if key not in destination_data:
                continue
            for addRow in addData[key]:
                destination_data[key].append(addRow)
                didModifyDestinationData = True

    if didModifyDestinationData:
        with open(destination_json_full_path, 'w') as destination_file:
            json.dump(destination_data, destination_file)
