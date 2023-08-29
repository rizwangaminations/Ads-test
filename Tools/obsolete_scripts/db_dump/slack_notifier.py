import subprocess
import os
from pprint import pprint
from slackclient import SlackClient
from slacker import Slacker

IGNORED_FILES = ['desktop.ini', 'thumbs.db', '.ds_store',
                 'icon\r', '.dropbox', '.dropbox.attr']

def is_ignored(filename):
    filename_lower = filename.lower()
    for ignored_file in IGNORED_FILES:
        if ignored_file in filename_lower:
            return True
    return False

def run():
    errorFilePath = os.path.dirname(os.path.abspath(__file__)) + "/Error.txt"
    logFilePath = os.path.dirname(os.path.abspath(__file__)) + "/Dump_Process_Log_File.txt"

    if os.path.isfile(errorFilePath):
        send_error_message(logFilePath);
    else:
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/dump"
        print(filepath)
        lastNE = "1"
        for filename in os.listdir(filepath):
            if is_ignored(filename):
                continue
            else:
                currentNENumber = filename.split('-')[1]
                if currentNENumber > lastNE:
                    lastNE = currentNENumber

        send_message_to_slack(lastNE, logFilePath);

def send_message_to_slack(lastNE, logFilePath):
    token = "xoxb-84327387763-8bwMuuAJUhZo6mia578JsNUP"
    sc = SlackClient(token)
    
    chan = "C2FTAPP96"
    successText = "All NE-APPS backup has been taken and uploaded to drop box - https://www.dropbox.com/home/megarama%20-%20db%20backups and last NE added was NE-" + lastNE
    print(sc.api_call("chat.postMessage", as_user="false:", channel=chan, text=successText, link_names="https://www.dropbox.com/home/megarama%20-%20db%20backups", icon_url="http://lorempixel.com/48/48", unfurl_links="false:"))

def send_error_message(logFilePath):
    token = "xoxb-84327387763-8bwMuuAJUhZo6mia578JsNUP"
    sc = SlackClient(token)
    slack = Slacker(token)
    
    chan = "C2FTAPP96"
    response = slack.files.upload(logFilePath, "", "", "", "DB BACKUPS LOG FILE", "Error while taking db backups see attached log file for more details", chan)

# -- RUN -- #
run()
