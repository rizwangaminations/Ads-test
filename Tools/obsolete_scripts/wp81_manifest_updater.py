import argparse, os
import re

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file_path', type=str, default="../proj.win8.1-universal/App.WindowsPhone/Package.appxmanifest", help="Input WP8.1 manifest file")
    arg_parser.add_argument('-b', '--build_number', type=int, help="Build number")
    args = arg_parser.parse_args()

    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_full_path = os.path.join(script_dir, args.file_path)

        substitutions = [ ["(<.*Identity.*Version=\"\d+\.)(\d+\.)(\d+\.)(\d+)(.*)","\g<1>\g<2>\g<3>" + str(args.build_number) + "\g<5>"] ]

        f = open(file_full_path, 'r+')
        content = f.read();

        for sub in substitutions:
            print(("Replacing '%s' with '%s'" % (sub[0], sub[1])))
            pattern = re.compile(sub[0]);
            content = pattern.sub(sub[1], content)

        f.seek(0)
        f.truncate();
        f.write(content)

    except Exception as e:
        print(("ERROR changing manifest file %s (%s)" % (args.file_path, str(e)) ))
