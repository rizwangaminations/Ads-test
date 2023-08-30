import os, sys
import shutil
import argparse
import io, re


def join_path(*args):
    return os.path.normpath(os.path.join(*args))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-s', '--source', type=str, help="Input source")
    arg_parser.add_argument('-d', '--destination', type=str, help="Input destination")
    args = arg_parser.parse_args()

    print(args.source)
    print(args.destination)


    script_dir = os.path.dirname(os.path.realpath(__file__))
    destination_path = join_path(script_dir, args.destination)
    source_path = join_path(script_dir, args.source)

    if not os.path.exists(source_path):
        print_error("Source path does not exist. Skipping ")
        sys.exit(1)
    if not os.path.exists(destination_path):
        print_error("Destination path does not exist. Skipping ")
        sys.exit(1)



    libsList = ['flatbuffers.a', 'libaudio.a', 'libc3d.a', 'libcc_core.a', 'libcc.a', 'libccandroid.a', 'libccb.a', 'libccds.a', 'libccs.a', 'libcpufeatures.a', 'libets.a', 'libext_pvmp3dec.a', 'libext_vorbisidec.a', 'libnet.a', 'librecast.a', 'libspine.a', 'libui.a']

    for lib_name in libsList:
        s = os.path.join(source_path, lib_name)
        d = os.path.join(destination_path, lib_name)
        shutil.copyfile(s, d)





