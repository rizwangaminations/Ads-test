SCRIPT_DIR="$( dirname "$0" )"


echo -----ANDROID BUILD----------------------------------
echo Starting Android armeabi-v7a
python $SCRIPT_DIR/../Tools/gradle_build.py -b release --supported_abi=armeabi-v7a  --proj_dir=$SCRIPT_DIR/
echo Completed armeabi-v7a

python $SCRIPT_DIR/copy_libs.py -d=$SCRIPT_DIR/../cocos2d/prebuilt/android/armeabi-v7a/ -s=$SCRIPT_DIR/app/build/intermediates/cxx/Release/3a3v703z/obj/local/armeabi-v7a/

echo Starting Android arm64-v8a
python $SCRIPT_DIR/../Tools/gradle_build.py -b release --supported_abi=arm64-v8a  --proj_dir=$SCRIPT_DIR/
echo Completed arm64-v8a



python $SCRIPT_DIR/copy_libs.py -d=$SCRIPT_DIR/../cocos2d/prebuilt/android/arm64-v8a/ -s=$SCRIPT_DIR/app/build/intermediates/cxx/Release/3a3v703z/obj/local/arm64-v8a
echo Copied android libs!!!!
