import os, sys
import argparse
import print_utils
import io, re
import hashlib
import string

LOGGER = print_utils.Logger()
Blue = print_utils.bcolors.OKBLUE
Fail = print_utils.bcolors.FAIL

sectionFolderName = 'CustomSections'
numberOfSections = 0
fileNames_list = []
sectionNames_list = []
fileContent_list = []

configFileName = 'Config_ios.xcconfig'
sectionString = '-sectcreate __TEXT __'
productName = ""

def join_path(*args):
    return os.path.normpath(os.path.join(*args))

def getEncryptedString(key):
    string_to_encrypt = key + productName
    encript1 = hashlib.md5(string_to_encrypt.encode())
    encrypted_string = encript1.hexdigest()
    return encript1.hexdigest()

def generateFileNames():
    for i in range(numberOfSections):
        name = getEncryptedString("file%i" % i)
        fileNames_list.append(name+'.txt')

        content = getEncryptedString("content%i" % i)
        fileContent_list.append(content)
    
def generateSectionName():
    for i in range(numberOfSections):
        name = getEncryptedString("section%i" % i)
        sectionNames_list.append(name)

def createFiles():
    sectionFolderPath = join_path(output_root_dir, sectionFolderName)
    if os.path.isdir(sectionFolderPath) == False:
        try:
            os.mkdir(sectionFolderPath)
        except OSError:
            print ("Creation of the sections directory failed exiting")
            quit()

    for i in range(numberOfSections):
        filepath = join_path(sectionFolderPath, fileNames_list[i])
        f= open(filepath,"w+")
        f.write(fileContent_list[i])
        f.close()
        LOGGER.i("file created at path: %s" % (filepath), 0 , Blue)

def updateConfigs():
    configFilePath = join_path(output_root_dir,configFileName)
    appendString = '\nSECTION_OTHER_LDFLAGS = $(inherited)'
    for i in range(numberOfSections):
        appendString = appendString + ' ' +sectionString + sectionNames_list[i] + ' ios/%s/'%sectionFolderName + fileNames_list[i]

    f=open(configFilePath, "a+")
    f.write(appendString);
    f.close()

if __name__ == '__main__':

    LOGGER.h("Installing XLRD python library...")
    try:
        os.system("pip install xlrd")
        import xlrd
        LOGGER.i("Python XLRD INSTALLED", 4)
    except:
        LOGGER.d("Failed to install XLRD python library")
        exit(0)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--xlsx_file', type=str, default="keys.xlsx", help="Input xlsx config file")
    arg_parser.add_argument('-d', '--dir', type=str, default="MiniGameData", help="working MiniGameData directory")
    args = arg_parser.parse_args()
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_root_dir = join_path(script_dir, args.dir)

    xlsx_full_path = join_path(output_root_dir, args.xlsx_file)
    configFilePath = join_path(output_root_dir, configFileName)

    LOGGER.h("Parsing %s file" % xlsx_full_path)
    rb = xlrd.open_workbook(xlsx_full_path, formatting_info=False)
    sheet = rb.sheet_by_index(0)
    for rowIdx in range(1, sheet.nrows):
        row = sheet.row(rowIdx)
        keys = row[2].value
        if keys == "-" or keys == "":
            numberOfSections = 0
            continue
        for key in keys.split(";"):
            if keys == "SECTION_COUNT":
                numberOfSections = int(row[3].value)

    configFile = open(configFilePath).read()
    lines = configFile.splitlines()
    for line in lines:
        if 'PRODUCT_NAME' in line:
            productName = line.split('=',1)[1].strip()

    if 'SECTION_OTHER_LDFLAGS' in configFile or numberOfSections <= 0:
        LOGGER.i("Sections already exist or not needed", 0 , Fail)
    else:
        generateFileNames()
        generateSectionName()
        createFiles()
        updateConfigs()


