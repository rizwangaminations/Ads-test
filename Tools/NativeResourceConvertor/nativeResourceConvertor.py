import os, sys, io
import argparse
import json
import ntpath
import fnmatch
import plistlib

def run_command(command):
    try:
        os.system(command)
    except Exception as inst:
        print(("Unable to execute '%s'. Exception: %s" % (command, str(inst))))


def join_path(*args):
    return os.path.normpath(os.path.join(*args))



def compressImage(imageDirectory, imageName):
    command = 'etcpack "%s/%s" "%s" -c etc1 -ext PNG -as' % (imageDirectory, imageName, imageDirectory)
    run_command(command)

def renameImage(fileNameWithPath):
    os.rename(fileNameWithPath, fileNameWithPath.replace('_alpha.pkm','.pkm@alpha'))
def removePNG(filePath):
    os.remove(filePath)

def processPNG(imageFullPath):
    if os.path.isfile(imageFullPath):
        imageDirectory, imageName = ntpath.split(imageFullPath)
        compressImage(imageDirectory, imageName)
        renameImage(imageFullPath.replace('.png','_alpha.pkm'))
        removePNG(imageFullPath)

def shouldExcludeFile(pngFullPath, excludedList):
    for excludedPNG in excludedList:
        if excludedPNG in pngFullpath:
            return True
    return False

def savePNGFilesinPlist(pngNameList, plistFilePath):
    if os.path.isfile(plistFilePath):
        os.remove(plistFilePath)
    new_file = io.open(plistFilePath , mode='w', newline='\n')
    new_file.close()
    output_dict = dict(
        nativeImages = list(pngNameList)
    )
    with open(plistFilePath, 'rb') as fp:
        plistlib.writePlist(output_dict, plistFilePath)




if __name__ == '__main__':



    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.environ["PATH"] = os.environ["PATH"] + ":" + join_path(script_dir, "Compression/")

    
    resources_default_path = join_path(script_dir, "../../Resources/")
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-j', '--json_config', type=str, default="native_excluded.json", help="Input json config file")
    arg_parser.add_argument('-r', '--resource_path', type=str, default=resources_default_path, help="Input Resources Path to Convert")
    args = arg_parser.parse_args()

    json_full_path = join_path(script_dir, args.json_config)
    resources_full_path = args.resource_path

#Creating list of excluded folders
    excludedList = []
    normalisedExcludedList = []
    if os.path.isfile(json_full_path):
        with open(json_full_path) as config_file:
            data = json.load(config_file)
            if "exclude" in data:
                excludedList = data["exclude"]

        for path in excludedList:
            normalisedPath = os.path.normpath(path)
            normalisedExcludedList.append(normalisedPath)


#Creating list of all PNGs in Resoruce folder
    pngsFilesWithPathToConvert = []
    for root, dirs, files in os.walk(resources_full_path):
        for file in files:
            if file.endswith(".png"):
                pngFullpath = os.path.join(root, file)
                if not shouldExcludeFile(pngFullpath, normalisedExcludedList):
                    pngsFilesWithPathToConvert.append(pngFullpath)


#Compress Selected PNGs
    for pngFile in pngsFilesWithPathToConvert:
        processPNG(pngFile)

