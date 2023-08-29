import os
import json, http.client, requests
import argparse
import print_utils
import custom_plistlib
import common_utils
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import zipfile
import shutil
import copy
import subprocess
import re

LOGGER = print_utils.Logger()
            
class ParseConfig:
    def __init__(self, source_parse_url, source_parse_app_id, source_parse_api_key, source_parse_master_key, destination_parse_url, destination_parse_app_id, destination_parse_api_key, destination_parse_master_key, working_dir, config_data):
    
        self.source_app_id = source_parse_app_id
        self.source_api_key = source_parse_api_key
        self.source_master_key = source_parse_master_key
        self.source_url = source_parse_url
        self.destination_app_id = destination_parse_app_id
        self.destination_api_key = destination_parse_api_key
        self.destination_master_key = destination_parse_master_key
        self.destination_url = destination_parse_url
        self.working_dir = working_dir
        self.config_data = config_data
        self.sync_rows_map = dict()
        self.source_data_map = dict()
    
    def syncParse(self):
        if "cleanup_destination_parse" in config_data and config_data["cleanup_destination_parse"] is True:
            self.cleanupDestinationParseSchemas()
        if "sync_parse_schema" in config_data and config_data["sync_parse_schema"] is True:
            self.syncParseScehma()
        if "download_source_files" in config_data and config_data["download_source_files"] is True:
            self.downloadFilesData()
        if "create_native_bundles" in config_data and config_data["create_native_bundles"] is True:
            self.createNativeBundles()
        if "upload_data" in config_data and config_data["upload_data"] is True:
            self.uploadFilesData()
        
    def cleanupDestinationParseSchemas(self):
        for table in config_data["tables"]:
            source_class_name = table["source_class"]
            destination_class_name = table["destination_class"]
            print(("Cleaning Destination Table '%s' entity" % (destination_class_name)))
            
            data_entity = self.DataEntity(source_class_name, destination_class_name)
            data = data_entity.get_destination_parse_data(self)
            if data is not None:
                for row in data["results"]:
                    object_id = row["objectId"]
                    data_entity.remove_destination_parse_data(self, object_id)
                
    def syncParseScehma(self):
        schema_entities = []
        for table in config_data["tables"]:
            source_class_name = table["source_class"]
            destination_class_name = table["destination_class"]
            schema_entities.append(self.SchemaEntity(source_class_name, destination_class_name))
            
        for entity in schema_entities:
            print(("Syncing Schema'%s' entity" % (entity.source_class_name)))
            data = entity.get_source_parse_data(self)
            entity.remove_destination_parse_data(self)
            data["className"] = entity.destination_class_name
            del data["classLevelPermissions"]
            del data["fields"]["ACL"]
            del data["fields"]["createdAt"]
            del data["fields"]["updatedAt"]
            del data["fields"]["objectId"]
            if "indexes" in  data: del data["indexes"]
            entity.post_parse_data(self, data)
            
    def getRowsData(self):
        data_entities = []
        for table in config_data["tables"]:
            source_class_name = table["source_class"]
            destination_class_name = table["destination_class"]
            self.sync_rows_map[source_class_name] = dict()
            data_entities.append(self.DataEntity(source_class_name, destination_class_name))
            
        for entity in data_entities:
            print(("Fetching Config For '%s' entity" % (entity.source_class_name)))
            data = entity.get_source_parse_data(self)
            self.source_data_map[entity.source_class_name] = data
                
    def downloadFilesData(self):
        file_entities = []
        for table in config_data["tables"]:
            source_class_name = table["source_class"]
            file_save_root_path = common_utils.join_path(self.working_dir, source_class_name)
            if not os.path.exists(file_save_root_path):
                os.makedirs(file_save_root_path)
            
            if not type(self.source_data_map) is dict or source_class_name not in self.source_data_map:
                self.getRowsData()
            data = self.source_data_map[source_class_name]
            
            for row in data["results"]:
                object_id = row["objectId"]
                file_save_row_root_path = common_utils.join_path(file_save_root_path, object_id)
                if not os.path.exists(file_save_row_root_path):
                    os.makedirs(file_save_row_root_path)
                for key, value in list(row.items()):
                    if type(value) is dict and "__type" in value  and value["__type"] == "File":
                        file_save_full_path = file_save_row_root_path + "/" + key + self.get_extension(value["url"])
                        if not os.path.isfile(file_save_full_path):
                            file_entities.append(self.FileEntity(source_class_name, file_save_full_path, value["url"]))
        
        total_files_to_download = len(file_entities)
        currently_downloading = 1
        for entity in file_entities:
            print(("Downloading File %d of %d:'%s'" % (currently_downloading, total_files_to_download, entity.file_url)))
            data = entity.get_source_parse_data(self)
            currently_downloading = currently_downloading + 1
            if not data:
                LOGGER.e("Downloading File Failed: %s" % (entity.file_url))
                
    def createNativeBundles(self):
        for table in config_data["tables"]:
            source_class_name = table["source_class"]
            file_save_root_path = common_utils.join_path(self.working_dir, source_class_name)
            if not type(self.source_data_map) is dict or source_class_name not in self.source_data_map:
                self.getRowsData()
            data = self.source_data_map[source_class_name]
            for row in data["results"]:
                object_id = row["objectId"]
                file_save_row_root_path = common_utils.join_path(file_save_root_path, object_id)
                for key, value in list(row.items()):
                    if type(value) is dict and "__type" in value  and value["__type"] == "File":
                        file_save_full_path = file_save_row_root_path + "/" + key + self.get_extension(value["url"])
                        if file_save_full_path.count('SD.zip') > 0  or file_save_full_path.count('HD.zip') > 0 or file_save_full_path.count('HDR.zip') > 0:
                            native_file_full_path = file_save_row_root_path + "/" + key + "_Native" + self.get_extension(value["url"])
                            if not os.path.isfile(native_file_full_path) and os.path.isfile(file_save_full_path):
                                self.create_native_zip(file_save_full_path)
                            
        
    def uploadFilesData(self):
        for table in config_data["tables"]:
            source_class_name = table["source_class"]
            destination_class_name = table["destination_class"]
            
            source_class_name = table["source_class"]
            destination_class_name = table["destination_class"]
            
            name_field = ""
            strings_replacer = dict()
            if "name_field" in table:
                name_field = table["name_field"]
            
            if "strings_replacer" in table:
                strings_replacer = table["strings_replacer"]
            
            file_save_root_path = common_utils.join_path(self.working_dir, source_class_name)
            if not type(self.source_data_map) is dict or source_class_name not in self.source_data_map:
                self.getRowsData()
            data = self.source_data_map[source_class_name]
            total_rows_to_upload = len(data["results"])
            currently_uploading = 1
            for row in data["results"]:
                print(("Uploading %s Table Row %d of %d" % (destination_class_name, currently_uploading, total_rows_to_upload)))
                object_id = row["objectId"]
                file_save_row_root_path = common_utils.join_path(file_save_root_path, object_id)
                
                file_name = "Empty"
                LOGGER.h("Processing objectId: %s" % object_id)
                if name_field != "" and name_field in row:
                    file_name = row[name_field]
                
                
                for item in os.listdir(file_save_row_root_path):
                    if item != '.DS_Store':
                        name, ext = os.path.splitext(item)
                        file_full_path = file_save_row_root_path + "/" + item
                        if os.path.isfile(file_full_path):
                            full_renamed_temp_path = self.rename_zip(file_save_row_root_path, item, file_name, strings_replacer)
                            file_entity = self.FileEntity(source_class_name, full_renamed_temp_path, "", name)
                            response = file_entity.put_parse_data(self)
                            if response is not None:
                                row[name] = response[name]
                                
                            os.remove(full_renamed_temp_path)
                del row["createdAt"]
                del row["objectId"]
                del row["updatedAt"]
                entity = self.DataEntity(source_class_name, destination_class_name)
                result_json = entity.post_parse_data(self, row)
                currently_uploading = currently_uploading + 1

                            
    def create_native_zip(self, zip_path):
        name, ext = os.path.splitext(zip_path)
        new_name = name + '_Native'
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
          zip_ref.extractall(name)
        
        self.clean_folder(name)
        self.convert_to_native(name)
        shutil.make_archive(new_name, 'zip', name)
        shutil.rmtree(name)

    def convert_to_native(self, folder_path):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        tool_script_path = os.path.join(script_dir, "NativeResourceConvertor", "nativeResourceConvertor.py")
        self.run_py(tool_script_path, '--resource_path=' + folder_path)
        
    def rename_zip(self, folder_path, old_name, prefix, strings_replacer):
        full_old_name = common_utils.join_path(folder_path, old_name)
        name, ext = os.path.splitext(old_name)
        new_name = self.replace_strings(strings_replacer, name)
        new_name = new_name + '_' + str(prefix) + ext
        new_name = re.sub(r"[^a-zA-Z0-9._]+", '', new_name)
        full_new_name = common_utils.join_path(folder_path, new_name)
        if os.path.isfile(full_old_name):
            shutil.copy(full_old_name, full_new_name)
        return full_new_name
    
    def run_py(self, script, *args):
        args_list = ['python', script]
        for arg in args:
            args_list.append(arg)
        subprocess.Popen(args_list).communicate()
    
    def clean_folder(self, folder_path):
        for name in os.listdir(folder_path):
            path_name = os.path.join(folder_path, name)
            if os.path.isdir(path_name) and name.endswith("__MACOSX"):
                shutil.rmtree(path_name)
            elif os.path.isfile(path_name) and name.endswith('.DS_Store'):
                os.remove(path_name)
        
    def replace_strings(self, strings_replacer, file_name):
        if len(strings_replacer) > 0:
            for key, value in list(strings_replacer.items()):
                file_name = file_name.replace(key, value)
        return file_name

    def get_extension(self, url):
        name, ext = os.path.splitext(url)
        return ext
        
    def check_availability(self):
        source_url = "%s/classes/User" % (self.source_url)
        destination_url = "%s/classes/User" % (self.destination_url)
        source_response = requests.get(source_url, headers=self.get_http_headers(self.source_app_id, self.source_api_key, self.source_master_key, "application/json"))
        destination_response = requests.get(destination_url, headers=self.get_http_headers(self.destination_app_id, self.destination_api_key, self.destination_master_key, "application/json"))
        if source_response.status_code >= 200 and source_response.status_code <= 300 and destination_response.status_code >= 200 and destination_response.status_code <= 300:
            return True
        else:
            print("Parse isn't accessible")
        return False
        
    def get_http_headers(self, app_id, api_key, master_key, content_type = "application/json"):
        return {
            "Content-Type" : content_type,
            "X-Parse-Application-Id": app_id,
            "X-Parse-REST-API-Key": api_key,
            "X-Parse-Master-Key": master_key
        }
    class FileEntity:
        def __init__(self, source_class_name, file_save_path, file_url, column_name = "None"):
            self.source_class_name = source_class_name
            self.file_save_path = file_save_path
            self.file_url = file_url
            self.column_name = column_name
            
        def get_source_parse_data(self, parse_config):
            retries = 3
            download_successful = True
            if os.path.isfile(self.file_save_path):
                return download_successful
            
            try:
                request = urllib.request.urlopen(self.file_url, timeout=60)
                with open(self.file_save_path, 'wb') as f:
                    try:
                        f.write(request.read())
                    except:
                        if retries > 0:
                            LOGGER.w("Failed download, retrying...")
                            retries -= 1
                            download_file(file_path, file_url)
                        else:
                            LOGGER.e("Request timed out, skipped file %s" % (file_url))
                            download_successful = False
            except:
                download_successful = False
                
            return download_successful
        def put_parse_data(self, parse_config):
            if os.path.isfile(self.file_save_path):
                current_file_name = os.path.basename(self.file_save_path)
                modified_file_name = current_file_name.replace(" ", "")
                dir_name = os.path.dirname(os.path.abspath(self.file_save_path))
                new_full_path = common_utils.join_path(dir_name, current_file_name.replace(current_file_name, modified_file_name))
                os.rename(self.file_save_path, new_full_path)
                self.file_save_path = new_full_path
        
            file_path = self.file_save_path
            file_name = os.path.basename(file_path)
            file_name = file_name.replace('&','')
            file_name = file_name.replace('\'','')

            #build request to upload file
            url = "%s/files/%s" % (parse_config.destination_url, file_name)
            print(("Uploading File: " + url))
            #load binary data from file and post it
            with open(file_path,'rb') as payload:
                response = requests.post(url, headers=parse_config.get_http_headers(parse_config.destination_app_id, parse_config.destination_api_key, parse_config.destination_master_key, "application/x-www-form-urlencoded"), data=payload)
            #check response. Successfull one should contain 'url' and 'name' keys for uploaded file
            if response.status_code >= 200 and response.status_code <= 300:
                response_json = json.loads(response.text)
#                print("%s uploaded to %s" % (file_name, response_json["url"]), 4)
                return {
                    self.column_name : {
                                    "__type" : 'File',
                                    "name" : response_json['name'],
                                    "url" : response_json['url']
                                }
                }
            else:
                LOGGER.e("Failed to upload %s (%s)" % (self.file_save_path, response.text))
            return None
    
    
    class DataEntity:
        def __init__(self, source_class_name, destination_class_name):
            self.source_class_name = source_class_name
            self.destination_class_name = destination_class_name

        def get_source_parse_data(self, parse_config):
            source_class_url = parse_config.source_url + "classes/" + self.source_class_name
            params = {'limit': 500}
            response = requests.get(source_class_url, params=params, headers=parse_config.get_http_headers(parse_config.source_app_id, parse_config.source_api_key, parse_config.source_master_key, "application/json"))
            if response.status_code >= 200 and response.status_code <= 300:
                response_json = json.loads(response.text)
                return response_json
            return None
        def get_destination_parse_data(self, parse_config):
            destination_class_url = parse_config.destination_url + "classes/" + self.destination_class_name
            params = {'limit': 500}
            response = requests.get(destination_class_url, params=params, headers=parse_config.get_http_headers(parse_config.destination_app_id, parse_config.destination_api_key, parse_config.destination_master_key, "application/json"))
            if response.status_code >= 200 and response.status_code <= 300:
                response_json = json.loads(response.text)
                return response_json
            return None
        def post_parse_data(self, parse_config, data):
            destination_data_url = parse_config.destination_url + "classes/" + self.destination_class_name
            response = requests.post(destination_data_url, headers=parse_config.get_http_headers(parse_config.destination_app_id, parse_config.destination_api_key, parse_config.destination_master_key, "application/json"), data=json.dumps(data))

            if response.status_code >= 200 and response.status_code <= 300:
                result = json.loads(response.text)
                return result
            else:
                LOGGER.e("Post Parse Config failed (%s): %d - %s" % (destination_data_url, response.status_code, response.text))
            return None
        def remove_destination_parse_data(self, parse_config, object_id):
            destination_data_url = parse_config.destination_url + "classes/" + self.destination_class_name + "/" + object_id
            response = requests.delete(destination_data_url, headers=parse_config.get_http_headers(parse_config.destination_app_id, parse_config.destination_api_key, parse_config.destination_master_key, "application/json"), data="")
#
            if response.status_code >= 200 and response.status_code <= 300:
                result = json.loads(response.text)
                return result
            else:
                LOGGER.e("Removing Destintion Parse Request failed (%s): %d - %s" % (destination_data_url, response.status_code, response.text))
            return None
            
    class SchemaEntity:
        def __init__(self, source_class_name, destination_class_name):
            self.source_class_name = source_class_name
            self.destination_class_name = destination_class_name

        def get_source_parse_data(self, parse_config):
            source_schema_url = parse_config.source_url + "schemas/" + self.source_class_name
            source_schema_response = requests.get(source_schema_url, headers=parse_config.get_http_headers(parse_config.source_app_id, parse_config.source_api_key, parse_config.source_master_key, "application/json"))
            if source_schema_response.status_code >= 200 and source_schema_response.status_code <= 300:
                response_json = json.loads(source_schema_response.text)
                return response_json
            return None
        def post_parse_data(self, parse_config, schema):
#            raise "Method not implemented. Should override!!!"
            destination_schema_url = parse_config.destination_url + "schemas/" + self.destination_class_name
            response = requests.post(destination_schema_url, headers=parse_config.get_http_headers(parse_config.destination_app_id, parse_config.destination_api_key, parse_config.destination_master_key, "application/json"), data=json.dumps(schema, separators=(',', ':')))

            if response.status_code >= 200 and response.status_code <= 300:
                result = json.loads(response.text)
            else:
                LOGGER.e("Schema Posting Request failed (%s): %d - %s" % (destination_schema_url, response.status_code, response.text))
            return None
        def remove_destination_parse_data(self, parse_config):
            destination_schema_url = parse_config.destination_url + "schemas/" + self.destination_class_name
            response = requests.delete(destination_schema_url, headers=parse_config.get_http_headers(parse_config.destination_app_id, parse_config.destination_api_key, parse_config.destination_master_key, "application/json"))

            if response.status_code >= 200 and response.status_code <= 300:
                result = json.loads(response.text)
            else:
                LOGGER.e("Removing Schema Request failed (%s): %d - %s" % (destination_schema_url, response.status_code, response.text))
            return None

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-j', '--json', type=str, default="copy_config.json",
                            help="Input json file with Parse sync configuration")
    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    json_full_path = common_utils.join_path(script_dir, args.json)

    LOGGER.i("Loading configuration data from %s" % (json_full_path))
    with open(json_full_path) as config_file:
        config_data = json.load(config_file)
    source_parse_url = config_data["source_parse_url"]
    source_parse_app_id = config_data["source_parse_app_id"]
    source_parse_api_key = config_data["source_parse_api_key"]
    source_parse_master_key = config_data["source_parse_master_key"]
    destination_parse_url = config_data["destination_parse_url"]
    destination_parse_app_id = config_data["destination_parse_app_id"]
    destination_parse_api_key = config_data["destination_parse_api_key"]
    destination_parse_master_key = config_data["destination_parse_master_key"]
    
    LOGGER.h("Source Parse URL: %s" % source_parse_url)
    LOGGER.h("Source Parse App ID: %s" % source_parse_app_id)
    LOGGER.h("Source Parse API Key: %s" % source_parse_api_key)
    LOGGER.h("Source Parse API Key: %s" % source_parse_master_key)
    LOGGER.h("Destination Parse URL: %s" % destination_parse_url)
    LOGGER.h("Destination Parse App ID: %s" % destination_parse_app_id)
    LOGGER.h("Destination Parse API Key: %s" % destination_parse_api_key)
    LOGGER.h("Destination Parse API Key: %s" % destination_parse_master_key)

    json_dir = common_utils.join_path(os.path.dirname(json_full_path), "CopyParseTablesData")
    LOGGER.h("Working Directory: %s" % json_dir)
    
    parse_config = ParseConfig(source_parse_url, source_parse_app_id, source_parse_api_key, source_parse_master_key, destination_parse_url, destination_parse_app_id, destination_parse_api_key, destination_parse_master_key, json_dir, config_data)
        
    parse_config.syncParse()
