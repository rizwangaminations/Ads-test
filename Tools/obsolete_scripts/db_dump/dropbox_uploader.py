import argparse, os
import dropbox, datetime


auth_token = "44vNrjZWn6AAAAAAAAAACAfSrg08FZJEJ0b3gyOZk88_CwcplBCQUYc5PDoDGbBy" #sol token

IGNORED_FILES = ['desktop.ini', 'thumbs.db', '.ds_store',
                 'icon\r', '.dropbox', '.dropbox.attr']

def is_ignored(filename):
    filename_lower = filename.lower()
    for ignored_file in IGNORED_FILES:
        if ignored_file in filename_lower:
            return True
    return False

if __name__ == '__main__':

    filepath = os.path.dirname(os.path.abspath(__file__)) + "/Dump_Process_Log_File.txt"
    errorFilePath = os.path.dirname(os.path.abspath(__file__)) + "/Error.txt"
    file = open(filepath,'a')
    file.write('\n\n/////////// Starting logs for dropbox uploader//////////')

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file_path', type=str, default="dump", help="File to upload")
    arg_parser.add_argument('-o', '--output_folder', type=str, default="Megarama - DB Backups/Automatic Backup", help="DropBox output folder")
    args = arg_parser.parse_args()

    client = dropbox.client.DropboxClient(auth_token)
    file.write('\nUploader: linked account: %s' % (client.account_info()))
    folder_metadata = client.metadata(args.output_folder)
    file.write('\nUploader: Metadata received')
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_full_path = os.path.join(script_dir, args.file_path)
        args.output_folder = args.output_folder + "/" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file.write('\nUploader: Path on which file will be uploaded %s' % (args.output_folder))
        
        for root, dirs, files in os.walk(file_full_path):
            path_to_append = root.replace(file_full_path, "")
            
            for filename in files:
                if is_ignored(filename):
                    continue
                file.write('\nUploader: Filename %s' %(filename))
                
                # construct the full local path
                local_path = os.path.join(file_full_path, root, filename)
                file.write('\nUploader: File local Path %s' %(local_path))

                # construct full dropbox path
                path_to_append = path_to_append.replace("\\", '/')
                
                dropbox_path = args.output_folder + path_to_append + "/" + filename
                file.write('\nUploader: Upload the file to %s' %(dropbox_path))
                
                

                statinfo = os.stat(local_path)
                if statinfo.st_size == 0:
                    with open(local_path, 'rb') as f:
                        response = client.put_file(dropbox_path, f)
                        file.write('\nUploader: UPLOAD FILE:%s\nRESPONSE:%s' %(args.file_path, response))
                else:
                    bigFile = open(local_path, 'rb')
                    uploader = client.get_chunked_uploader(bigFile, statinfo.st_size)

                    while uploader.offset < statinfo.st_size:
                        try:
                            upload = uploader.upload_chunked()
                        except rest.ErrorResponse as e:
                            error = open(errorFilePath,'w')
                            error.close()
                            file.write('\nUploader: Dropbox rest exception: %s' % (e))
                    uploader.finish(dropbox_path)
                    file.write('\nUploader: UPLOAD FILE %s' % (dropbox_path))
        file.close()

    except dropbox.rest.ErrorResponse as e:
        error = open(errorFilePath,'w')
        error.close()
        file.write('\nUploader: dropbox exception: %s' % (e))