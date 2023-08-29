@SETLOCAL
@echo off

echo -----Backing up %APP%-----

set SCRIPT_DIR=%~dp0
set INSTALL_DIR=%SCRIPT_DIR%/dump/%APP%
mongodump -h %URI% -d %USER_NAME% -u %USER_NAME% -p %PASSWORD% -o %INSTALL_DIR%