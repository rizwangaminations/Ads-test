#https://api.slack.com/docs/oauth-test-tokens go to the link to generate new token and replace it in line 8 (default_token)

import argparse
import requests
import time
import json

default_token = 'xoxp-8029040837-8028624528-54709289159-603f1ab7eb'

def list_files(token, ts_to_delete):
    params = {
        'ts_to': ts_to_delete,
        'token': token,
        'count': 1000
    }
    uri = 'https://slack.com/api/files.list'
    response = requests.post(uri, params=params)
    files = json.loads(response.text)['files']
    return files

def delete_files(token, files, attempts=3):
    for file in files:
        file_id = file["id"]
        file_name = file["name"]
        file_date = time.ctime(int(file["created"]))
        params = {
            'token': token,
            'file': file_id,
            'set_active': "true",
            '_attempts': str(attempts)
        }
        uri = 'https://slack.com/api/files.delete'
        response = requests.get(uri, params=params)
        print("Removing:", file_name, file_date, json.loads(response.text))

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--days', type=int, default=7, help="Files 'age' to be deleted")
    arg_parser.add_argument('-t', '--token', type=str, default=default_token, help="Slack access token")
    args = arg_parser.parse_args()

    #Delete files older than this:
    ts_to_delete = int(time.time()) - args.days * 24 * 60 * 60
    files = list_files(args.token, ts_to_delete)
    delete_files(args.token, files)