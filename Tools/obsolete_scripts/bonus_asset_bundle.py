#!/usr/bin/env python

import argparse
import sys, os, shutil
import requests, json
import print_utils
import common_utils
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import subprocess
from zipfile import ZipFile
from sets import Set

LOGGER = print_utils.Logger()

class FileTypes():
    def __init__(self, name, extension,extension2 = "notdefined"):
        self.name = name
        self.extension = extension
        self.extension2 = extension2

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not(self == other)

FileTypes.Csd = FileTypes("Csd","csd")
FileTypes.Csb = FileTypes("Csb","csb")
FileTypes.Ogg = FileTypes("Ogg","ogg")
FileTypes.Aiff = FileTypes("Aiff","aiff")
FileTypes.Particle = FileTypes("Paticle","plist")
FileTypes.Atlas = FileTypes("Atlas","plist")
FileTypes.Png = FileTypes("Png","png")
FileTypes.SpriteFrame = FileTypes("SpriteFrame","png","jpg")

sfx_path_ios     = "ios/sfx"
sfx_path_android = "android/sfx"
sfx_path_windows = "windows_phone/sfx"

gfx_path_hdr = "gfx/HDR"
gfx_path_hd  = "gfx/HD"
gfx_path_sd  = "gfx/SD" 

verbose = True

default_assets_json = [
        "nodeXp.csb", 
        "nodeCoins.csb", 
        "nodeGems.csb", 
        "nodeExtraPicks.csb", 
        "nodeNextRoundPicks.csb", 
        "nodeOutcomeMultiplier.csb", 
        "nodeNextRoundOutcomeMultiplier.csb", 
        "nodeJackpot.csb", 
        "nodeCompletesRound.csb", 
        "nodeLevelUp.csb", 
        "nodeWinAll.csb", 
        "nodeFreeSpinCount.csb",
        "nodeMultiplier.csb",
        "nodeXPMultiplier.csb",
        "nodeGameMode.csb",
        "IndicatorPanel.csb", 
        "CounterElement.csb",
        "nodeCloseButton.csb"
    ]

def get_files_in_folder(directory,recursive):
    file_paths = []  
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = join_path(root, filename)
            file_paths.append(filepath)
        if not recursive:
            return file_paths
    return file_paths

def join_path(path1,path2):
    return os.path.join(path1,path2)
    
def is_valid_file(json_key, file_name):
    return is_audio_file(json_key) or is_csb_file(file_name) or is_png_file(file_name)

def is_audio_file (json_key):        
    return "sfx" in json_key.lower() or "music" in json_key.lower() or "audio" in json_key.lower()

def is_csb_file (file_name):
    return file_name.lower().endswith(".csb")

def is_png_file (file_name):
    return file_name.lower().endswith(".png")

def is_string(value):
    return isinstance(value, str)

def is_dict(value):
    return isinstance(value, dict)

def is_list(value):
    return isinstance(value, list)

def is_parseable(value):
    return is_string(value) or is_dict(value) or is_list(value)

def hasExtension(filePath):
    name = os.path.basename(filePath)
    return name.rfind(".") != -1

def remove_extension(file_path):
    index = file_path.rindex(".")
    return file_path[0:index]

def replaceHDRResolution(path,isSd):
    if isSd:
        return path.replace(gfx_path_hdr,gfx_path_sd)
    else:
        return path.replace(gfx_path_hdr,gfx_path_hd)

class PathStructure:
    def __init__(self, relativePath, fullPath):
        self.relative_path = relativePath
        self.full_path = fullPath

    def __key(self):
        return (self.relative_path, self.full_path)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if other == None:
            return False
        return self.__key() == other.__key()

    def __ne__(self, other):
        return not(self == other)

class FilesFinder:
    def __init__(self, root_path): 
        self.root_path = root_path
        self.files_types = {}
        self.files_types[FileTypes.Csd] = {}
        self.files_types[FileTypes.Csb] = {}
        self.files_types[FileTypes.Aiff] = {}
        self.files_types[FileTypes.Ogg] = {}
        self.files_types[FileTypes.Particle] = {}
        self.files_types[FileTypes.Png] = {}
        self.files_types[FileTypes.Atlas] = {}
        self.files_types[FileTypes.SpriteFrame] = {}

    def find_files(self):
        self.add_found_files(FileTypes.Csd,"CocosProject/cocosstudio")
        self.add_found_files(FileTypes.Csb,"CSB")
        self.add_found_files(FileTypes.Aiff,"sfx/aiff")
        self.add_found_files(FileTypes.Ogg,"sfx/ogg")
        self.add_found_files(FileTypes.Particle,"Particles", True)
        self.add_found_files(FileTypes.Png,gfx_path_hdr)
        self.add_found_files(FileTypes.Atlas,gfx_path_hdr)
        self.add_found_files(FileTypes.SpriteFrame,"tps")

    def add_found_files(self,type, path, useRootPath = False ):
        currentPath = join_path(self.root_path,path)
        dict = self.files_types[type]
        for root, subFolders, files in os.walk(currentPath):
            for file in files:
                if file.endswith("." + type.extension) or file.endswith("." + type.extension2):
                    fullPath = join_path(root,file)
                    if useRootPath:
                        relativePath = fullPath.replace(self.root_path,"")
                    else:
                        relativePath = fullPath.replace(currentPath, "")
                    relativePath = relativePath[1:]
                    relativePath = relativePath.replace("\\","/")
                    fullPath = fullPath.replace("\\","/")   
                    path_structure = PathStructure(relativePath,fullPath)
                    if file in dict:
                        dict[file].append(path_structure)
                    else:
                        dict[file] = [path_structure]

    def print_elements(self):
        if verbose:
            for keyType in self.files_types:
                typeDict = self.files_types[keyType]
                for fileKey in typeDict:
                    values = typeDict[fileKey]
                    color = print_utils.bcolors.OKBLUE
                    if len(values) > 1:
                        color = print_utils.bcolors.OKGREEN
                    for value in values:
                        LOGGER.i("FilesFinder %s: %s->%s" % (keyType.name, fileKey, value.relative_path), 0 , color)

    def get_path(self,filePath,type,errorOnNotFound=True,errorOnDuplicate=True):
        dict = self.files_types[type]
        fileName = os.path.basename(filePath)
        if not hasExtension(fileName):
            fileName = fileName + "." + type.extension
        if not fileName in dict:
            if errorOnNotFound:            
                LOGGER.e("Missing resources type:%s: name:%s path:%s" % (type.name, fileName, filePath))
                sys.exit()
            else:
                return None
        values = dict[fileName]
        if len(values) > 1:
            for value in values:
                if value.relative_path == filePath:
                    return value
            if errorOnDuplicate:
                LOGGER.e("More than one resource found %s, 1:%s, 2%s" %(filePath, values[0].relative_path, values[1].relative_path))
                sys.exit()
        return values[0]

class SpriteFramesFinder:
    def __init__(self):
        self.sprite_frames = {}

    def parse_plists(self, plists_dict):
        for plist in list(plists_dict.values()):
            for path_structure in plist:
                self.parse_plist(path_structure.full_path)


    def parse_plist(self,plist_path):
        tree = ET.parse(plist_path)
        root = tree.getroot()
        for dict in root.findall("dict"):
            for dict2 in dict.findall("dict"):
                for key in dict2.findall("key"):
                    keyString = key.text
                    if keyString.endswith(".png"):
                        if keyString in self.sprite_frames:
                            self.sprite_frames[keyString].append(plist_path)
                        else:
                            self.sprite_frames[keyString] = [plist_path]

    def print_elements(self):
        if verbose:
            for key in self.sprite_frames:
                values = self.sprite_frames[key]
                color = print_utils.bcolors.OKBLUE
                if len(values) > 1:
                    color = print_utils.bcolors.OKGREEN
                for value in values:
                    LOGGER.i("SpriteFramesFinder: %s->%s" % (key, value), 0, color)

    def get_path(self,pngName):
        if not pngName in self.sprite_frames:
            if not pngName or pngName == "Default/Sprite.png" or pngName == "Default/ImageFile.png":
                return None
            else:
                LOGGER.e("Sprite frame not found %s" %(pngName))
                sys.exit()
        value = self.sprite_frames[pngName]
        if len(value) > 1:
            LOGGER.e("More than one resource found %s, 1:%s, 2%s" %(fileName, value[0], value[1]))
            sys.exit()
        return value[0]                


class AssetsCopier:
    def __init__(self,fileFinder,spriteFinder,assets_repacker,output_path):
        self.file_finder = fileFinder
        self.sprite_finder = spriteFinder
        self.assets_repacker = assets_repacker
        self.files_to_copy = set()
        self.not_confirmed_copy = set()
        self.output_path = output_path
        self.atlas_to_preload = set()

    def process_string(self,key,value):
        new_string = ""
        if is_audio_file(key):
            oggPath = self.file_finder.get_path(value,FileTypes.Ogg)
            aiffPath = self.file_finder.get_path(value,FileTypes.Aiff)
            self.save_file_to_copy(sfx_path_android,oggPath.relative_path, oggPath.full_path)
            self.save_file_to_copy(sfx_path_windows,oggPath.relative_path, oggPath.full_path)
            self.save_file_to_copy(sfx_path_ios,aiffPath.relative_path, aiffPath.full_path)
            new_string = remove_extension(aiffPath.relative_path)
        elif is_csb_file(value):
            csdTempPath = value.replace(".csb",".csd");
            new_string = self.find_and_parse_csd_resources(csdTempPath)
        elif is_png_file(value):
            new_string = self.find_and_process_image(value,"")
        else:
            new_string = value

        if not new_string:
            LOGGER.e("String not found old:%s new:%s" % (value, new_string))
            sys.exit()
        return new_string

    def save_file_to_copy(self,path_prefix, relative_path, absolutePath, confirmed_copy = True):        
        path_structure = PathStructure(join_path(path_prefix, relative_path),absolutePath)
        if confirmed_copy:
            self.files_to_copy.add(path_structure)
        else:
            self.not_confirmed_copy.add(path_structure)

    def set_preload(self, preload):
        self.atlas_to_preload = preload

    def clean_atlas_pendingToConfirm(self,confirm):
        if confirm:
            self.files_to_copy.update(self.not_confirmed_copy)
        else:
            self.not_confirmed_copy = set()

    def find_and_process_image(self,pngName,plistName):
        atlasInfo = None
        pngInfo = None

        isImageOnAtlas = True

        if plistName:
            atlasInfo = self.file_finder.get_path(plistName, FileTypes.Atlas)
            pngInfo = self.file_finder.get_path(plistName.replace(".plist",".png"),FileTypes.Png)
            isImageOnAtlas = True
        else:
            pngInfo = self.file_finder.get_path(pngName,FileTypes.Png,False)
            isImageOnAtlas = False
            if pngInfo == None:
                atlasPath = self.sprite_finder.get_path(pngName)
                if atlasPath != None:
                    atlasInfo = self.file_finder.get_path(atlasPath, FileTypes.Atlas)
                    pngInfo = self.file_finder.get_path(atlasPath.replace(".plist",".png"),FileTypes.Png)
                    isImageOnAtlas = True

        if pngInfo == None and atlasInfo == None:
            LOGGER.w("Neither atlas or png found png:%s, plist:%s" %(pngName,plistName))

        #we don't confirm pngs/atlas to be copied as they might be repacked later
        #we only confirm pngs without atlas like backgrounds
        if pngInfo != None:
            self.save_file_to_copy(gfx_path_hdr,pngInfo.relative_path, pngInfo.full_path, atlasInfo == None)
            self.save_file_to_copy(gfx_path_sd,pngInfo.relative_path, replaceHDRResolution(pngInfo.full_path,True), atlasInfo == None)
            self.save_file_to_copy(gfx_path_hd,pngInfo.relative_path, replaceHDRResolution(pngInfo.full_path,False), atlasInfo == None)
        if atlasInfo != None:
            self.atlas_to_preload.add(remove_extension(pngInfo.relative_path))
            self.save_file_to_copy(gfx_path_hdr,atlasInfo.relative_path, atlasInfo.full_path, False)
            self.save_file_to_copy(gfx_path_sd,atlasInfo.relative_path, replaceHDRResolution(atlasInfo.full_path,True), False)
            self.save_file_to_copy(gfx_path_hd,atlasInfo.relative_path, replaceHDRResolution(atlasInfo.full_path,False), False)

        if isImageOnAtlas:
            self.assets_repacker.addSprite(pngName)

        return pngInfo.relative_path if pngInfo != None and not isImageOnAtlas else pngName

    def find_and_parse_csd_resources(self, csdName):
        if verbose:
            LOGGER.i("Parsing csd resource %s" %(csdName))
        csdRealPath = self.file_finder.get_path(csdName, FileTypes.Csd)
        self.parse_csd(csdRealPath.full_path)
        csbName = csdName.replace(".csd",".csb")
        csbInfo = self.file_finder.get_path(csbName,FileTypes.Csb)
        self.save_file_to_copy("CSB",csbInfo.relative_path, csbInfo.full_path)
        return csbInfo.relative_path

    def parse_csd(self,file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        for abstract_node_data in root.iter('AbstractNodeData'):
            node_type = abstract_node_data.get("ctype")
            file_data = abstract_node_data.find("FileData")
            if file_data != None:
                plist = file_data.get("Plist")
                path  = file_data.get("Path")   
                if node_type == "ProjectNodeObjectData":
                    if path and path.lower().endswith(".csd"):
                        self.find_and_parse_csd_resources(path)
                if node_type == "ParticleObjectData":
                    if path:
                        particlePath = self.file_finder.get_path(path, FileTypes.Particle)
                        self.save_file_to_copy("",particlePath.relative_path, particlePath.full_path)
                elif node_type == "SpriteObjectData" or node_type == "ImageViewObjectData":      
                    self.find_and_process_image(path,plist)
            elif node_type == "ButtonObjectData":
                self.parseButtonData(abstract_node_data.find("DisabledFileData"))
                self.parseButtonData(abstract_node_data.find("PressedFileData"))
                self.parseButtonData(abstract_node_data.find("NormalFileData"))


    def parseButtonData(self,data):
        if data != None:
            plist = data.get("Plist")
            path  = data.get("Path")  
            if path and path != "Default/Button_Press.png":
                self.find_and_process_image(path,plist) 

    def copy_files(self):
        for path in self.files_to_copy:
            if verbose:
                LOGGER.i("copying file dest:%s origin:%s" % (path.relative_path, path.full_path))
            destination = join_path(self.output_path, path.relative_path)
            destinationDir = os.path.dirname(destination)
            if not os.path.isdir(destinationDir) or not os.path.exists(destinationDir):
                os.makedirs(destinationDir)
            shutil.copy(path.full_path, destination) 

class AssetsRepacker:
    def __init__(self,repackWanted,fileFinder,output_path):
        self.file_finder = fileFinder
        self.png_paths = set()
        self.repackWanted = repackWanted
        try:
            subprocess.call(["TexturePacker","--quiet"])
            self.texturePackerInstalled = True
        except OSError as e:
            print(e)
            self.texturePackerInstalled = False
         #os.system("command -v TexturePacker >/dev/null 2>&1 || { exit 1; }") == 0

    def canRepack(self):
        if self.repackWanted and not self.texturePackerInstalled:
            LOGGER.w("TexturePacker not installed, skipping repack")
        return self.repackWanted and self.texturePackerInstalled

    def addSprite(self,spriteName):
        if self.repackWanted:            
            pngPath = self.file_finder.get_path(spriteName,FileTypes.SpriteFrame,True,False)
            self.png_paths.add(pngPath.full_path)

    def repackAtlas(self):
        atlasName = "BonusAtlas"
        command = "TexturePacker "
        for sprite in self.png_paths:
            command += "'" + sprite + "' "
        command += "--sheet " + output_path + "/gfx/{v}/" + atlasName + "{n}.png "
        command += "--data " + output_path + "/gfx/{v}/"+ atlasName + "{n}.plist "
        command += "--max-width 2048 "
        command += "--max-height 2048 "
        command += "--multipack "
        command += "--format cocos2d-v2 "
        command += "--variant 1:HDR "
        command += "--variant 0.5:HD "
        command += "--variant 0.25:SD "
        #command += "--quiet "

        if verbose:
            LOGGER.i(command)

        os.system(command)

        atlas_preload = set()
        for num in range (10):
            atlas_preload.add(atlasName + str(num))

        return atlas_preload

class AssetsJsonParser:
    def __init__(self,copier):
        self.copier = copier

    def process_json(self,jsonPath):
        self.json_path = jsonPath
        with open(jsonPath) as json_file:
            self.json = json.load(json_file)
        self.addDefaults()
        self.parse_dict(self.json)

    def finish_json(self):
        self.update_json()
        self.write_json()

    def addDefaults(self):
        for resource in default_assets_json:
            self.process_string("",resource)

    def parse_dict(self,dict):
        for key in dict:
            value = dict[key]
            if is_string(value) and is_valid_file(key,value):
                result = self.process_string(key,value)
                dict[key] = result
            elif is_list(value):
                self.parse_list(key,value)
            elif is_dict(value):
                self.parse_dict(value)
            

    def parse_list(self,key,list):
        if key == "preload_resources":
            del list[:]
            return
        for idx in range(len(list)):
            value = list[idx]
            if is_dict(value):
                self.parse_dict(value)
            elif is_list(value):
                self.parse_list(value)
            elif is_string(value) and is_valid_file(key,value):
                result = self.process_string(key,value)
                list[idx] = result


    def process_string(self,key,value):
        return self.copier.process_string(key,value)

    def update_json(self):
        atlas = self.copier.atlas_to_preload
        preload = []
        preload.extend(atlas)
        self.json["preload_resources"] = preload

    
    def write_json(self):
        with open(self.json_path, "w") as json_file:
            json_file.write(json.dumps(self.json, indent=2, sort_keys=True))

class AssetsCompressor:
    def __init__(self,compress_tool):
        self.compress_tool = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image_utils", compress_tool + ".py")

    def do_compression(self,path):
        compression_command = self.compress_tool + ' --input_dir= ' + path + ' --output_dir= ' + path
        if verbose:
            LOGGER.i("compression command: %s" % (compression_command))
        common_utils.run_py(self.compress_tool, '--input_dir=' + path, '--output_dir=' + path)

class BonusZipper:
    def __init__(self):
        pass

    def zip_path(self, zip_path, filesToCompress, path_to_remove):
        zip_folder = os.path.dirname(zip_path)
        if not os.path.exists(zip_folder):
            os.makedirs(zip_folder)

        if os.path.isfile(zip_path):
            os.remove(zip_path)

        if verbose:
            LOGGER.i("creating zip file %s" % (zip_path))


        with ZipFile(zip_path,'w') as zip:
            for file in filesToCompress:
                file_zip_path = file.replace(path_to_remove,"")
                if zip_path == file:
                    LOGGER.w("zip file included on the target zip (recursive), skipping %s" %(zip_path))
                    continue
                if file.endswith(".zip"):
                    LOGGER.w("adding a zip file to target zip, it might be wrong, skipping %s" %(file))
                    continue
                if verbose:
                    LOGGER.i("adding zip file %s, %s" % (file_zip_path, file))
                zip.write(file, file_zip_path)  
            zip.close()  
           
    def build_zip_path(self,output_path, zipName):
        return join_path(output_path, zipName+".zip") 

    def zip_output(self, input_path, output_path):  
        filesCommon = get_files_in_folder(input_path,False)
        filesCommon.extend(get_files_in_folder(join_path(input_path,"CSB"),True))
        filesCommon.extend(get_files_in_folder(join_path(input_path,"Particles"),True))

        self.zip_path(self.build_zip_path(output_path,'bonusCommon'),     filesCommon, input_path)
        self.zip_path(self.build_zip_path(output_path,'androidSfx'),      get_files_in_folder(join_path(input_path,sfx_path_android), True),  join_path(input_path,sfx_path_android))
        self.zip_path(self.build_zip_path(output_path,'iosSfx'),          get_files_in_folder(join_path(input_path,sfx_path_ios), True),  join_path(input_path,sfx_path_ios))
        self.zip_path(self.build_zip_path(output_path,'windowsPhoneSfx'), get_files_in_folder(join_path(input_path,sfx_path_windows), True),  join_path(input_path,sfx_path_windows))
        self.zip_path(self.build_zip_path(output_path,'assetsHDR'),       get_files_in_folder(join_path(input_path,gfx_path_hdr), True),  join_path(input_path,gfx_path_hdr))
        self.zip_path(self.build_zip_path(output_path,'assetsHD'),        get_files_in_folder(join_path(input_path,gfx_path_hd), True),  join_path(input_path,gfx_path_hd))
        self.zip_path(self.build_zip_path(output_path,'assetsSD'),        get_files_in_folder(join_path(input_path,gfx_path_sd), True),  join_path(input_path,gfx_path_sd))
                 

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-r', '--repo_root_path', type=str, help="Videoslotbank repo root path", required = True)
    arg_parser.add_argument('-j', '--json_path', type=str, help="BonusGame-Asset json path", required = True)
    arg_parser.add_argument('-o', '--output_path', type=str, help="Output path, where files are going to be copied, optional, if not defined it uses json_path by default", default="")
    arg_parser.add_argument('-q', '--quiet', action='store_true', help="Disables verbose", default = False)
    arg_parser.add_argument('-t', '--compress_tool', type=str, help="Compression tool. 'pngquant' is used by default", default = "pngquant")
    arg_parser.add_argument('-c', '--compress', action='store_true', help="Enables graphics compression. Disabled by default")
    arg_parser.add_argument('-rp', '--repack', action='store_true', help="Repacks all game atlas in a single atlas", default = False)
    arg_parser.add_argument('-z', '--zip', action='store_true', help="Enables Zip compression. Disabled by default")
    arg_parser.add_argument('-zp', '--zip_path', type=str, help="defines the zip path, output_path/parse by default")
    args = arg_parser.parse_args()

    verbose = not args.quiet

    bonusRootFolder = join_path(args.repo_root_path, "Bank - Generic Bonus Game")
    if not os.path.isdir(bonusRootFolder) or not os.path.exists(bonusRootFolder):
        LOGGER.e("Bonus root folder not found under Videoslotbank")
        sys.exit()

    fileFinder = FilesFinder(bonusRootFolder)
    fileFinder.find_files()
    fileFinder.print_elements();

    spriteFinder = SpriteFramesFinder()
    spriteFinder.parse_plists(fileFinder.files_types[FileTypes.Atlas])
    spriteFinder.print_elements();

    output_path = args.output_path
    if not output_path:
        output_path = os.path.dirname(args.json_path)

    assetsRepacker = AssetsRepacker(args.repack,fileFinder,output_path)

    assetsCopier = AssetsCopier(fileFinder,spriteFinder,assetsRepacker,output_path)

    parser = AssetsJsonParser(assetsCopier)
    parser.process_json(args.json_path)

    assetsCopier.clean_atlas_pendingToConfirm(not assetsRepacker.canRepack())

    if assetsRepacker.canRepack():
        preload = assetsRepacker.repackAtlas()
        assetsCopier.set_preload(preload)

    parser.finish_json()

    assetsCopier.copy_files()

    if args.compress:
        compressor = AssetsCompressor(args.compress_tool)
        compressor.do_compression(output_path)

    if args.zip:        
        zip_path = join_path(output_path, "parse")
        if args.zip_path:
            zip_path = args.zip_path
        zipper = BonusZipper()
        zipper.zip_output(output_path,zip_path)


