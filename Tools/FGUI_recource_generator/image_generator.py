import os, sys
import shutil
import argparse
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


def setup_fairygui_files(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if file.endswith(".png") and "FUI" in os.path.join(root, file):
                    path_for_HDR = os.path.join(root, file).replace("FUI", "HDR")
                    path_for_HD = os.path.join(root, file).replace("FUI", "HD")
                    path_for_SD = os.path.join(root, file).replace("FUI", "SD")

                    create_dir(path_for_HDR)
                    create_dir(path_for_HD)
                    create_dir(path_for_SD)
                    
                    print(("Generating HDR, HD and SD Variants for PNG: " + os.path.join(root, file)))
                    hdr_image = Image.open(os.path.join(root, file))
                    width, height = hdr_image.size;
                    hd_image = hdr_image.resize((max(1, int(round(width*0.5))), max(1, int(round(height*0.5)))), Image.ANTIALIAS)
                    sd_image = hdr_image.resize((max(1, int(round(width*0.25))), max(1, int(round(height*0.25)))), Image.ANTIALIAS)
                    hdr_image.save(path_for_HDR)
                    hd_image.save(path_for_HD)
                    sd_image.save(path_for_SD)
    

if __name__ == '__main__':

    script_dir = os.path.dirname(os.path.realpath(__file__))
    resource_folder_path = join_path(script_dir, "FUI")

    if not os.path.exists(resource_folder_path):
        print_error("Resource folder does not exist.")
        sys.exit()
    else:
        setup_fairygui_files(resource_folder_path)
        remove_dir(resource_folder_path)
        print ("Images generated")

