import argparse
import os
from fnmatch import fnmatch

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--dir', type=str, default="", help="Search directory")
    arg_parser.add_argument('-e', '--extensions', type=str, default="*.*", help="File extension")
    args = arg_parser.parse_args()


    script_dir = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(script_dir, args.dir)

    extensions = args.extensions.split(" ")
    found_files = []
    for path, subdirs, files in os.walk(full_path):
        for name in files:
            for extension in extensions:
                if fnmatch(name, extension):
                    found_files.append(os.path.join(path, name))
                    break

    newest = max(found_files, key=lambda file_path: os.stat(file_path).st_mtime )

    print(newest)