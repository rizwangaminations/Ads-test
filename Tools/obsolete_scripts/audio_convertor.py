import argparse, os
import fnmatch

def create_dir(path):
    try:
        os.makedirs(path)
    except:
        pass

def get_file_name(filename):
    ret = ".".join(os.path.basename(filename).split('.')[:-1])
    return ret

def run_command(command):
    try:
        os.system(command)
    except Exception as inst:
        print(("Unable to execute '%s'. Exception: %s" % (command, str(inst))))

def convert_caf(input_file, output_folder):
    #read more info on https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/afconvert.1.html
    output_file = os.path.join(output_folder, get_file_name(input_file) + ".caf")
    print(("    CAF: Converting %s -> %s" % (input_file, output_file)))
    command = 'afconvert -f %s -d %s@%i -c 1 "%s" "%s"' % ("caff", "ima4", 24000, input_file, output_file)
    create_dir(output_folder)
    run_command(command)

def convert_aiff(input_file, output_folder):
    #read more info on https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/afconvert.1.html
    output_file = os.path.join(output_folder, get_file_name(input_file) + ".aiff")
    print(("    AIFF: Converting %s -> %s" % (input_file, output_file)))
    command = 'afconvert -f %s -d %s@%i -c 1 "%s" "%s"' % ("AIFC", "ima4", 24000, input_file, output_file)
    create_dir(output_folder)
    run_command(command)

def convert_ogg(input_file, output_folder):
    #read more infor about ffmpeg https://trac.ffmpeg.org/wiki/Encode/MP3
    output_file = os.path.join(output_folder, get_file_name(input_file) + ".ogg")
    print(("    OGG: Converting %s -> %s" % (input_file, output_file)))
    command = 'ffmpeg -i "%s" -c:a libvorbis -v 8 -y -q:a 0 -ac 1 "%s"' % (input_file, output_file)
    create_dir(output_folder)
    run_command(command)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--input_folder', type=str, default="", help="Input folder")
    arg_parser.add_argument('-f', '--file_masks', type=str, default="*.wav", help="Files search masks. Comma-separated")
    args = arg_parser.parse_args()

    print("------------Installing dependencies----------")
    run_command('ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    run_command("brew install ffmpeg --with-libvorbis")

    convertors = [
        #["caf", convert_caf],
        ["ogg", convert_ogg],
        ["aiff", convert_aiff]
    ]
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_folder = os.path.normpath(os.path.join(script_dir, args.input_folder))

    input_files = []
    input_files_masks = args.file_masks.split(',')
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            for mask in input_files_masks:
                if fnmatch.fnmatch(file, mask):
                    input_file = os.path.normpath(os.path.join(root, file))
                    input_files.append(input_file)
    print(("------------Converting sounds (%s) in folder %s-----------" % (str(input_files_masks), input_folder)))
    for output_type, convertor in convertors:
        for input_file in input_files:
            file_folder = os.path.dirname(input_file)
            output_folder = file_folder.replace(input_folder, os.path.join(input_folder, output_type))
            convertor(input_file, output_folder)
    print("------------Converting sounds DONE-----------")


