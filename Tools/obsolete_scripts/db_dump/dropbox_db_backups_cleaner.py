import argparse, os
import dropbox, datetime
auth_token = "44vNrjZWn6AAAAAAAAAACAfSrg08FZJEJ0b3gyOZk88_CwcplBCQUYc5PDoDGbBy"
last_backups_needed = 14

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
    file.write('\n\n\n/////////// Starting logs for dropbox_db_backups_cleaner//////////\n')
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file_path', type=str, default="dump", help="File to upload")
    arg_parser.add_argument('-o', '--dropbox_dir', type=str, default="Megarama - DB Backups/Automatic Backup", help="DropBox dump dir")
    args = arg_parser.parse_args()

    client = dropbox.client.DropboxClient(auth_token)
    file.write('Cleaner: Authorized\n')

    script_dir = os.path.dirname(os.path.realpath(__file__))
    dropbox_folder = args.dropbox_dir
    
    try:
        response = client.metadata(dropbox_folder, list=True, file_limit=25000, hash=None, rev=None, include_deleted=False, include_media_info=False)
        file.write('Cleaner: Meta data received\n')

        backupsArray = response['contents']
        backupArrayLength = len(backupsArray)
        file.write('Cleaner: Total backups %s' %(backupArrayLength))
        if backupArrayLength>last_backups_needed:
            backUpNeedsDeletion = backupArrayLength-last_backups_needed
            file.write('\nCleaner: Folders need deletion %s' % (backUpNeedsDeletion))
            for i in range(0,backUpNeedsDeletion):
                file.write('\nCleaner: Deleting %s' % (backupsArray[i]["path"]))
                file_delete_response = client.file_delete(backupsArray[i]["path"])
                file.write('\nCleaner: Deleted %s' % (file_delete_response))
        file.close()
    except Exception as e:
        error = open(errorFilePath,'w')
        error.close()
        file.write('Cleaner: Exception in deleting folder %s' % (e) )
