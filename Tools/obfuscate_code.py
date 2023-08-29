import os, sys
import shutil
import argparse
import json
import filecmp
import fnmatch
import zipfile
import random
from random import randrange
import string
import fileinput
import plistlib
import io, re
import hashlib
from shutil import move
from tempfile import mkstemp
from os import fdopen, remove
import importlib

obfuscated_strings_map = {}
dictionary_words = {}

def join_path(*arg):
    return os.path.normpath(os.path.join(*arg))

def load_words(dir_path):
    valid_words = list('test')
    all_words = list()
    with open(dir_path + '/obfuscate_words.txt') as word_file:
        all_words = list(word_file.read().split())

    # Filter all non alpha numeric words
    for word in all_words:
        if word.isalnum:
            valid_words.append(word)
    return valid_words


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_random_dictionary_word():
    # return "Test"
    random_index = randrange(len(dictionary_words))
    return dictionary_words[random_index]

def obfuscate_string(source_string, prefix, postfix):
    string_to_split = source_string[len(prefix): len(source_string) - len(postfix)]
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', string_to_split)
    split_words = [m.group(0) for m in matches]
    
    final_word = get_random_dictionary_word()
    is_first_word = True
    for word in split_words:
        word_to_insert = get_random_dictionary_word()
        if is_first_word:
            word = word.capitalize()
            is_first_word = False
        final_word = final_word + word + word_to_insert.capitalize()

    return final_word

def get_obfuscated_string_for_string(source_string, prefix, postfix):
    replaced_string = ""
    if source_string in obfuscated_strings_map:
        replaced_string = obfuscated_strings_map[source_string]
    else:
        replaced_string = obfuscate_string(source_string, prefix, postfix)
        obfuscated_strings_map[source_string] = replaced_string
    return replaced_string

def get_obfuscate_config_data(dir_path):
    obfuscate_config = {}
    with open( dir_path + '/obfuscate_code_config.json') as json_file:
        obfuscate_config = json.load(json_file)
    return obfuscate_config

def get_obfuscated_line_for_prefix_postfix(line, prefix, postfix):
    new_line = line
    start_index = 0
    first_key_index = line.find(prefix, start_index)
    while first_key_index != -1:
        second_key_index = line.find(postfix, first_key_index + len(prefix))
        if second_key_index != -1:
            string_to_replace = line[first_key_index:second_key_index + len(postfix)]
            replaced_string = get_obfuscated_string_for_string(string_to_replace, prefix, postfix)

            new_line = new_line.replace(string_to_replace , replaced_string)
            has_modified_file = True
        else: 
            break;
        start_index = second_key_index + len(postfix)
        first_key_index = line.find(prefix, start_index)
    return new_line


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    obfuscate_strings_map_file_path = dir_path + '/../../MiniGameData/obfuscated_string.json'

    obfuscate_config = get_obfuscate_config_data(dir_path)
    dictionary_words = load_words(dir_path)

    if os.path.isfile(obfuscate_strings_map_file_path):
        with open(obfuscate_strings_map_file_path) as infile:
            obfuscated_strings_map = json.load(infile)

    project_dir = dir_path + "/../"
    search_file_extentions = ['.h' , '.cpp', '.mm', '.java']


    code_prefix = obfuscate_config["prefix"]
    code_postfix = obfuscate_config["postfix"]
    code_exclude_list = obfuscate_config["excluded_dir"]

    for r, d, f in os.walk(project_dir):
        for file in f:
            if any(s in file for s in search_file_extentions):
                full_file_path = join_path(r, file)
                if any(s in full_file_path for s in code_exclude_list):
                    continue
                file_lines = []
                has_modified_file = False

                with open(full_file_path, "r", encoding='ISO-8859-1') as f:
                    for line in f:
                        new_line = line;
                        new_line = get_obfuscated_line_for_prefix_postfix(new_line, code_prefix, code_postfix)
                        if line != new_line:
                            has_modified_file = True

                        file_lines.append(new_line)
                if has_modified_file:
                    print(("Modified File: "+full_file_path))
                    file_writer = open(full_file_path, "w")
                    for line in file_lines:
                        file_writer.write(line)
                    file_writer.close()

    #Storing Obfuscation data for future releases
    if obfuscated_strings_map:
        with open(obfuscate_strings_map_file_path, 'w') as fp:
            json.dump(obfuscated_strings_map, fp)
    










    
