import os, sys, glob
import shutil
import argparse
import json
import filecmp
import fnmatch
try:
    import PIL
except:
    os.system("python -m pip install Pillow")
from PIL import Image
from PIL import PngImagePlugin

LARGE_ENOUGH_NUMBER = 10
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024**2)

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


def check_masks(filename, masks):
    return any(fnmatch.fnmatch(filename.lower(), mask) for mask in masks)

def join_path(*arg):
    return os.path.normpath(os.path.join(*arg))

def create_dir(path):
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def remove_dir(path):
    try:
        shutil.rmtree(path)
    except Exception as e:
        print_error("Failed to delete %s: %s" % (path, str(e)))

def copy_file(src, dest, inc_masks, exc_masks):
    if check_masks(src, inc_masks) and not check_masks(src, exc_masks):
        try:
            create_dir(dest)
            shutil.copyfile(src, dest)
#            print("    %s -> %s" % (src, dest))
        except Exception as e:
            print_error('COPY_FILE Error: %s' % str(e))


def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        if name != '.DS_Store':
            print_info("DIFFERENT: %s" % os.path.join(dcmp.right, name))
#    for name in dcmp.right_only:
#        if name != '.DS_Store':
#            print_info("DEST ONLY: %s" % os.path.join(dcmp.right, name))
    for sub_dcmp in list(dcmp.subdirs.values()):
        print_diff_files(sub_dcmp)

def merge_dirs(src, dst, inc_masks = ["*.*"], exc_masks = [], symlinks=False, ignore=None, fileType=''):
    if not os.path.exists(src):
        print_warning("%s not exists. Skipping" % (src))
        return
    if os.path.isdir(src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                merge_dirs(s, d, inc_masks, exc_masks, symlinks, ignore)
            else:
                copy_file(s, d, inc_masks, exc_masks)
    else:
        copy_file(src, dst, inc_masks, exc_masks)

def compare_dirs(src, dst):
    if os.path.isdir(src):
        dcmp = filecmp.dircmp(src, dst, ['.DS_Store'])
        print_diff_files(dcmp)
    else:
        if filecmp.cmp(src, dst) == False:
            print_info("DIFFERENT: %s" %dst)


class SyncEntity:
    def __init__(self, json_dir, json_node, resource_Type):
        self.source_path = "" if "from" not in json_node else join_path(json_dir, json_node["from"])
        self.dest_path   = "" if "to" not in json_node else join_path(json_dir, json_node["to"])
        self.comment     = "" if "comment" not in json_node else json_node["comment"]
        self.resourceTypes = ["default"] if "type" not in json_node else json_node["type"]
        masks = [] if "masks" not in json_node else json_node["masks"]
        self.selectedResourceType = resource_Type


        exclude_masks = []
        include_masks = []
        self.files_to_check = []
        self.files_to_delete = []
        
        self.check_and_removed_existing_fairygui_resources()
        self.setup_fairygui_files()
        
        for mask in masks:
            if mask.startswith('~'):
                exclude_masks.append(mask.replace('~', ''))
            else:
                include_masks.append(mask)

        self.include_masks = ["*.*"] if len(include_masks)==0 else [join_path(self.source_path, mask).lower() for mask in include_masks]
        self.exclude_masks = [] if len(exclude_masks)==0 else [join_path(self.source_path, mask).lower() for mask in exclude_masks]
    
    def setup_fairygui_files(self):
        for root, dirs, files in os.walk(self.source_path):
            for file in files:
                if file.endswith(".png") and "FUI" in os.path.join(root, file):
                    path_for_HDR = os.path.join(root, file).replace("FUI", "HDR")
                    path_for_HD = os.path.join(root, file).replace("FUI", "HD")
                    path_for_SD = os.path.join(root, file).replace("FUI", "SD")
                    
                    print(("Generating HDR, HD and SD Variants for PNG: " + os.path.join(root, file)))
                    hdr_image = Image.open(os.path.join(root, file))
                    width, height = hdr_image.size;
                    hd_image = hdr_image.resize((max(1, int(round(width*0.5))), max(1, int(round(height*0.5)))), Image.Resampling.LANCZOS)
                    sd_image = hdr_image.resize((max(1, int(round(width*0.25))), max(1, int(round(height*0.25)))), Image.Resampling.LANCZOS)
                    hdr_image.save(path_for_HDR)
                    hd_image.save(path_for_HD)
                    sd_image.save(path_for_SD)
                    self.remove_file(os.path.join(root, file))
                    
    def check_and_removed_existing_fairygui_resources(self):
        for root, dirs, files in os.walk(self.source_path):
            for file in files:
                if file.endswith(".png") and "FUI" in os.path.join(root, file):
                    file_path = os.path.join(root, file)
                    sep = 'atlas'
                    stripped_file_name = file_path.split(sep, 1)[0] + sep
                    self.files_to_check.append(stripped_file_name)

        self.files_to_check = list(dict.fromkeys(self.files_to_check))
        for fileName in self.files_to_check:
            self.remove_resources(fileName)


    def remove_resources(self, file_name):
        path_for_HDR = file_name.replace("FUI", "HDR")
        # print(path_for_HDR)

        for filename_HDR in glob.glob(path_for_HDR + "*"):
            filename_HD = filename_HDR.replace("HDR", "HD")
            filename_SD = filename_HDR.replace("HDR", "SD")
            self.files_to_delete.extend([filename_HDR, filename_HD, filename_SD])
        
        self.files_to_delete = list(dict.fromkeys(self.files_to_delete))
        for file_path in self.files_to_delete:
            self.remove_file(file_path)

    def remove_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def merge(self):
        #print_info("MERGE(\n    %s -> %s\n    %s,\n    INCLUDE: %s\n    EXCLUDE: %s\n)" % (self.source_path, self.dest_path, self.comment, str(self.include_masks), str(self.exclude_masks)))
        for type in self.resourceTypes:
            if type == 'default' or self.selectedResourceType[type]:
                merge_dirs(self.source_path, self.dest_path, self.include_masks, self.exclude_masks)

    def compare(self):
#        print_info("COMPARE(\n    %s\n): %s -> %s" % (self.comment, self.source_path, self.dest_path))
        compare_dirs(self.source_path, self.dest_path)




if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-j', '--json_config', type=str, help="Input json config file")
    arg_parser.add_argument('-g', '--game_type', type=str, help="Input game type json file")
    arg_parser.add_argument('-a', '--action', type=str, choices=["merge", "compare"], default="merge", help="Action to perform for directories")
    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_full_path = join_path(script_dir, args.json_config)
    json_dir = os.path.dirname(json_full_path)

    resourceType = {}
    if args.game_type:
        game_type_json_full_path = join_path(script_dir, args.game_type)
        game_type_json_dir = os.path.dirname(game_type_json_full_path)

        with open(game_type_json_full_path) as config_file:   
            resourceType = json.load(config_file)
            
        print_info("Features = %s" % (resourceType))

    functors = {
        "compare" : lambda entity: entity.compare(),
        "merge"   : lambda entity: entity.merge()
    }

    with open(json_full_path) as config_file:   
        data = json.load(config_file)
        if args.action == "merge" and "clean" in data:
            for folder in data["clean"]:
                folder_full_path = join_path(json_dir, folder)
#                print_info("Deleting %s" % (folder_full_path))
                remove_dir(folder_full_path)
        for source in data["sources"]:
            syncEntity = SyncEntity(json_dir, source, resourceType)
            functors[args.action](syncEntity)
