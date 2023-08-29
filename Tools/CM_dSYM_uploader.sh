#!/bin/sh

PROJ_ROOT=$FCI_BUILD_DIR/GameRoot/proj.ios_mac
ARTIFECT_PATH=$FCI_BUILD_OUTPUT_DIR

if [ ! -d "$PROJ_ROOT" ]; then
  PROJ_ROOT=$FCI_BUILD_DIR/proj.ios_mac
fi

PODS_ROOT=$PROJ_ROOT/Pods
GOOGLE_SERVICE_PLIST_PATH=$PROJ_ROOT/ios/GoogleService-Info.plist

zipFile="$(find ${ARTIFECT_PATH} -iname "*.zip")"
mkdir all_dSYM
unzip ${zipFile} -d all_dSYM
dSYMFile="$(find all_dSYM -iname "*.app.dSYM")"

echo "PODS_ROOT: ${PODS_ROOT}"
echo "dSYM File: $dSYMFile"
echo "Zip File: ${zipFile}"

$PODS_ROOT/FirebaseCrashlytics/upload-symbols -gsp $GOOGLE_SERVICE_PLIST_PATH -p ios $FCI_BUILD_DIR/$dSYMFile

exit 0

