import argparse, os
import dropbox
import requests

auth_token = "44vNrjZWn6AAAAAAAAAACAfSrg08FZJEJ0b3gyOZk88_CwcplBCQUYc5PDoDGbBy"

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--dropbox_dir', type=str, default="Megarama - Scrum Team/Android Builds", help="Dropbox directory to clean")
    arg_parser.add_argument('-n', '--remain_files', type=int, default=3, help="Amount of files to remain in dropbox folder")
    args = arg_parser.parse_args()

    try:
        os.system("pip install dropbox")
        print("Python DROPBOX INSTALLED")
    except:
        print("Error installing DROPBOX python library")
        exit(0)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    dropbox_folder = args.dropbox_dir
    client = dropbox.client.DropboxClient(auth_token)
    #print 'linked account: ', client.account_info()
    try:
        response = client.metadata(dropbox_folder, list=True, file_limit=25000, hash=None, rev=None, include_deleted=False, include_media_info=False)
        print(response)
    except:
        print(("ERROR to upload %s" % (args.file_path) ))
