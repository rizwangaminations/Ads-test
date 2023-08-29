@echo off

SET SCRIPT_DIR=%~dp0

:Backing up locally:
python %SCRIPT_DIR%/db_backups.py

:Deleting extra backups from dropbox:
python %SCRIPT_DIR%/dropbox_db_backups_cleaner.py

:Uploading to dropbox:
python %SCRIPT_DIR%/dropbox_uploader.py

:Notify slack channel:
python %SCRIPT_DIR%/slack_notifier.py