import argparse, os
import dropbox
import print_utils

auth_token = "44vNrjZWn6AAAAAAAAAACAfSrg08FZJEJ0b3gyOZk88_CwcplBCQUYc5PDoDGbBy"

LOGGER = print_utils.Logger()

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file_path', type=str, help="File to upload")
    arg_parser.add_argument('-o', '--output_folder', type=str, help="DropBox output folder")
    args = arg_parser.parse_args()

    try:
        os.system("pip install dropbox")
        LOGGER.h("Python DROPBOX INSTALLED")
    except:
        LOGGER.e("Error installing DROPBOX python library")
        exit(0)
    
    client = dropbox.Dropbox(auth_token)
    print('linked account: ', client.users_get_current_account())
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_full_path = os.path.join(script_dir, args.file_path)
        f = open(file_full_path, 'rb')
        file_name = os.path.basename(file_full_path)
        dropbox_path = args.output_folder + '/' + file_name
        LOGGER.h("UPLOADING FILE '%s' to '%s'" % (file_full_path, dropbox_path))
        response = client.files_upload(f, dropbox_path)
        LOGGER.i("UPLOAD FILE DONE : RESPONSE:\n%s" %(response))
    except Exception as e:
        LOGGER.e("ERROR to upload '%s' to '%s' (%s)" % (args.file_path, args.output_folder, str(e)))
