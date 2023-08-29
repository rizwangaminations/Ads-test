import os
import shutil

def nextPowerOf2(x):
    x = x - 1;
    x = x | (x >> 1)
    x = x | (x >> 2)
    x = x | (x >> 4)
    x = x | (x >> 8)
    x = x | (x >>16)
    return x + 1

def checkCreateDir(dirName):
    try:
        os.stat(dirName)
    except:
        os.makedirs(dirName)