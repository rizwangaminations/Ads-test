import os
import json, httplib, requests
import argparse
import print_utils
import zipfile
import common_utils
import shutil

LOGGER = print_utils.Logger()

class ParseConfig:

    class DataEntity:
        def __init__(self, json_node):
            self.skip = json_node["skip"] if "skip" in json_node else False              
            self.key = json_node["key"]
            self.comment = json_node["comment"] if "comment" in json_node else "<NO INFO>"     

        def get_parse_data(self, parse_config):
            if self.skip:
                LOGGER.w("Entity '%s' is set to be skipped" % (self.key))
                return None
            return self.get_parse_data_impl(parse_config)

        def get_parse_data_impl(self, parse_config):
            raise "Method not implemented. Should override!!!"


    class FileEntity(DataEntity):
        def __init__(self, workingDir, json_node):
            ParseConfig.DataEntity.__init__(self, json_node)
            file_node = json_node['file']
            self.path = common_utils.join_path(workingDir, file_node['path'])
            self.compress = file_node['zip'] if "zip" in file_node else False

        def build_zip(self):
            file_base_name = os.path.basename(self.path)
            dir_name = os.path.dirname(self.path)
            zip_file_name = self.path + ".zip"
            LOGGER.i("Creating ZIP file %s" % (zip_file_name), 4)
            with zipfile.ZipFile(zip_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as ziph:
                for root, dirs, files in os.walk(self.path):
                    for file in files:
                        full_file_path = os.path.join(root, file)
                        #write file to ZIP. Remove root path from ZIP hierarchy
                        ziph.write(full_file_path, full_file_path.replace(self.path, ""))
            return zip_file_name         
        
        def get_parse_data_impl(self, parse_config):
            #check if dir exists
            if os.path.exists(self.path) == False:
                LOGGER.e("Path %s doesn't exist. SKIPPING entity!" % (self.path), 4)
                return None

            #Determine file full path to be uploaded to Parse (directly or compress Zip before)
            file_path = self.path if self.compress == False else self.build_zip()
            file_name = os.path.basename(file_path)
            #build request to upload file
            url = "%s/files/%s" % (parse_config.url, file_name)
            #load binary data from file and post it
            with open(file_path,'rb') as payload:
                response = requests.post(url, headers=parse_config.get_http_headers('application/x-www-form-urlencoded'), data=payload)
            #check response. Successfull one should contain 'url' and 'name' keys for uploaded file
            if response.status_code >= 200 and response.status_code <= 300:
                response_json = json.loads(response.text)
                LOGGER.i("%s uploaded to %s" % (file_name, response_json["url"]), 4)
                return {
                    self.key : {
                                    "__type" : 'File',
                                    "name" : response_json['name'],
                                    "url" : response_json['url']
                                }
                }
            else:
                LOGGER.e("Failed to upload %s (%s)" % (self.path, response.text), 4)
            return None

    class ValueEntity(DataEntity):
        def __init__(self, json_node):
            ParseConfig.DataEntity.__init__(self, json_node)
            self.value = json_node["value"]

        def get_parse_data_impl(self, parse_config):
            #just return json-formatted key-value pair
            return {
                self.key : self.value
            }

    def __init__(self, working_dir, json_doc):
        self.app_id = json_doc['parse_app_id']
        self.api_key = json_doc['parse_api_key']
        self.url = json_doc['parse_url']
        self.working_dir = working_dir
        self.entities = []
        for entity in json_doc['entities']:
            if "file" in entity:
                self.entities.append(self.FileEntity(self.working_dir, entity))
            if "value" in entity:
                self.entities.append(self.ValueEntity(entity))

    def get_http_headers(self, content_type = "application/json"):
        return {
            "Content-Type" : content_type,
            "X-Parse-Application-Id": self.app_id,
            "X-Parse-REST-API-Key": self.api_key
        }

    def check_availability(self):
        url = "%s/classes/User" % (self.url)    
        response = requests.get(url, headers=self.get_http_headers("application/json"))
        if response.status_code >= 200 and response.status_code <= 300:
            return True
        else:
            LOGGER.e("Parse isn't accessible (%s): %d - %s" % (url, response.status_code, response.text))
        return False

    def get_level_data(self, level_num):
        url = "%s/classes/Levels" % (self.url)
        response = requests.get(url, headers=self.get_http_headers("application/json"))
        if response.status_code >= 200 and response.status_code <= 300:
            result = json.loads(response.text)
            for levelData in result["results"]:
                if levelData["level"] == level_num:
                    return levelData
        else:
            LOGGER.e("Request failed (%s): %d - %s" % (url, response.status_code, response.text))
        return None

    def get_new_level_id(self):
        url = "%s/classes/Levels" % (self.url)
        response = requests.get(url, headers=self.get_http_headers("application/json"))
        max_level_id = -1
        if response.status_code >= 200 and response.status_code <= 300:
            result = json.loads(response.text)
            for levelData in result["results"]:
                level_id = levelData["level"]
                if level_id > max_level_id:
                    max_level_id = level_id
        else:
            LOGGER.e("Request failed (%s): %d - %s" % (url, response.status_code, response.text))
        return max_level_id + 1


    def create_record_for_level(self, level_num):
        url = "%s/classes/Levels" % (self.url)
        response = requests.post(url, headers=self.get_http_headers("application/json"), data=json.dumps({'level' : level_num, 'level_index' : level_num}))
        if response.status_code >= 200 and response.status_code <= 300:
            result = json.loads(response.text)
            print result
            return result['objectId'];
        else:
            LOGGER.e("Request failed (%s): %d - %s" % (url, response.status_code, response.text))
        return None

    def put_level_data(self, objectId, data):
        url = "%s/classes/Levels/%s" % (self.url, objectId)
        response = requests.put(url, headers=self.get_http_headers("application/json"), data=json.dumps(data))
        if response.status_code >= 200 and response.status_code <= 300:
            result = json.loads(response.text)
        else:
            LOGGER.e("Request failed (%s): %d - %s" % (url, response.status_code, response.text))
        return None   

    def upload(self, level):
        level_num = level
        #-1 means auto-detection for level id
        if level_num == -1:
            level_num = self.get_new_level_id()
            LOGGER.h("Level Number AUTODETECTED: %i" % (level_num))

        #Retrieve level data for specified level id
        levelData = self.get_level_data(level_num)
        #Check if level data exists and request data update
        common_utils.check_skip_task(levelData == None, "Level %d already exists:\n(%s).\nDo you really want to update it?" % (level_num, levelData))
        #Check if level data doesn't exist -> create new record for level and get it's 'objectId'
        if levelData == None:
            LOGGER.i("Uploading new level %d" % (level_num), 4)
            parse_object_id = self.create_record_for_level(level_num)
        #Level data already exists (level is on parse) -> get it's 'objectId'
        else:
            LOGGER.w("Updating existing level %d" % (level_num), 4)
            parse_object_id = levelData["objectId"]

        #build final dict with updating data
        parse_data = dict()
        for entity in self.entities:
            LOGGER.h("Processing '%s' entity (Comment:%s)" % (entity.key, entity.comment))
            data = entity.get_parse_data(self)
            #if data is not None -> merge it to final dictionary
            if data != None:
                parse_data.update(data)
        #put new data to Parse server
        print parse_data
        self.put_level_data(parse_object_id, parse_data)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-j', '--json', type=str, default="level_config.json", help="Input json file with level Parse sync configuration")
    arg_parser.add_argument('-l', '--level', type=int, default = -1, help="Level number to upload. -1 means autodetecting")
    arg_parser.add_argument('-c', '--compression_tool', type=str, default = "pngquant", help="Compression tool")
    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_full_path = common_utils.join_path(script_dir, args.json)
    json_dir_full_path = os.path.dirname(json_full_path)

    working_dir = json_dir_full_path
    #If resources should be compressed with PNGQUANT or etc. -> compress it to separate folder and process compressed one
    if args.compression_tool != "":
        working_dir = common_utils.join_path(json_dir_full_path, '_' + args.compression_tool)
        #Check/remove old directory
        if os.path.exists(working_dir):
            LOGGER.h("Removing old working directory %s" % (working_dir))
            shutil.rmtree(working_dir)
        #allocate Python script file in image_utils folder
        compression_tool_script = common_utils.join_path(script_dir, 'image_utils', args.compression_tool + '.py')
        #compress resources to working dir
        common_utils.run_py(compression_tool_script, '--input_dir=' + json_dir_full_path, '--output_dir=' + working_dir)

    LOGGER.i("Loading configuration data from %s" % (json_full_path))
    with open(json_full_path) as config_file:
        parse_config = ParseConfig(working_dir, json.load(config_file))

    LOGGER.h("Parse URL: %s" % parse_config.url)
    LOGGER.h("Parse App ID: %s" % parse_config.app_id)
    LOGGER.h("Parse API Key: %s" % parse_config.api_key)

    if parse_config.check_availability() == False:
        exit(0)

    parse_config.upload(args.level)
