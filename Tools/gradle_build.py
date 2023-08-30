import os
import json
import argparse
import common_utils
import print_utils
import re
import shutil

LOGGER = print_utils.Logger()


def build_gradle(project_dir, build_mode, supported_abi, extra_params, post_crashlytics, variant):
    gradlew_path = common_utils.join_path(project_dir, 'gradlew.bat' if os.name == "nt" else 'gradlew')
    gradlew_cmd = '"%s" %s -Ppost_crashlytics=%s  -Psupported_abi="%s" %s%s' % (gradlew_path, extra_params, post_crashlytics, supported_abi, variant, build_mode.capitalize())
    LOGGER.i("Running::2 %s" % (gradlew_cmd), 4)
    common_utils.run_command(gradlew_cmd, project_dir)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-b', '--build_mode', type=str, default="debug", help="Build mode")
    arg_parser.add_argument('-p', '--proj_dir', type=str, default="../proj.android-as", help="Project directory")
    arg_parser.add_argument('-g', '--gradle_params', type=str, default="", help="Addition gradle params")
    arg_parser.add_argument('-abi', '--supported_abi', type=str, default="armeabi-v7a", help="supported architectures")
    arg_parser.add_argument('-cr', '--post_crashlytics', type=str, default="true", help="Upload Crashlytics Symbols")
    arg_parser.add_argument('-v', '--variant', type=str, default="assemble", help="Defint build variant [assemble | bundle]")


    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = common_utils.join_path(script_dir, args.proj_dir)

    #GRADLE build
    LOGGER.h("Starting GRADLE build" + 30 * '-')
    build_gradle(project_dir, args.build_mode, args.supported_abi, args.gradle_params, args.post_crashlytics, args.variant)

