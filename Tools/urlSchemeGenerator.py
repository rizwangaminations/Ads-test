import os, sys
import argparse
import json
import print_utils
import io, re
import hashlib
import string
import plistlib
import random

LOGGER = print_utils.Logger()
Blue = print_utils.bcolors.OKBLUE
Fail = print_utils.bcolors.FAIL

numberOfSchemes = 41
productName = ""

def randomString(stringLength=20):
    letters = string.ascii_letters
    numbers = [6, 12, 23, 14, 16, 8]
    schemeKey = ''.join(random.choice(letters) for i in range(random.choice(numbers)))
    randomStr = getEncryptedString(schemeKey)[0:stringLength]
    index = 0
    encryptedString = ""

    for item in randomStr:
        if item.isdigit():
            if int(randomStr[index]) >= 0 and int(randomStr[index]) <= 9:
                repChar = random.choice(letters)
                encryptedString = ''.join([encryptedString,repChar])
                pass
        else:
            encryptedString = ''.join([encryptedString,randomStr[index]])
        
        index = index + 1

    return encryptedString

def join_path(*args):
    return os.path.normpath(os.path.join(*args))

def getEncryptedString(key):
    string_to_encrypt = key + productName
    encript1 = hashlib.md5(string_to_encrypt.encode())
    encrypted_string = encript1.hexdigest()
    return encrypted_string

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
    URL_SCHEMES = []

    url_schemes_file_path = script_dir + '/../../MiniGameData/urlSchemes.json'

    if os.path.isfile(url_schemes_file_path):
        with open(url_schemes_file_path) as infile:
            URL_SCHEMES = json.load(infile)

    rb = xlrd.open_workbook(xlsx_full_path, formatting_info=False)
    sheet = rb.sheet_by_index(0)
    for rowIdx in range(1, sheet.nrows):
        row = sheet.row(rowIdx)
        keys = row[2].value
        if keys == "-" or keys == "":
            continue
        for key in keys.split(";"):
            if key == "PACKAGE_NAME":
                productName = row[3].value
                LOGGER.i("product Name: %s" % productName)
            elif key == "DUMMY_URL_SCHEME_COUNT":
                if row[3].value.isdigit():
                    numberOfSchemes = int(row[3].value)
                    pass
                LOGGER.i("Number Of Schemes: %s" % numberOfSchemes)

    if not URL_SCHEMES or len(URL_SCHEMES) < numberOfSchemes:
        LOGGER.i("generating new schemens")
        for x in range(abs(numberOfSchemes-len(URL_SCHEMES))):
            URL_SCHEMES.append(randomString())
            pass

    ios_plist_file = join_path(output_root_dir, "ios/Info.plist")
    with open(ios_plist_file, 'rb') as fp:
        ios_plist_data = plistlib.load(fp)

    plist_url_arr = ios_plist_data["LSApplicationQueriesSchemes"]

    for scheme in URL_SCHEMES:
        plist_url_arr.append(scheme)
        print(scheme)

    plist_url_arr = list(dict.fromkeys(plist_url_arr))

    ios_plist_data["LSApplicationQueriesSchemes"] = plist_url_arr
    with open(ios_plist_file, 'wb') as fp:
        plistlib.dump(ios_plist_data, fp)

    with open(url_schemes_file_path, 'w') as fp:
        json.dump(URL_SCHEMES, fp)

