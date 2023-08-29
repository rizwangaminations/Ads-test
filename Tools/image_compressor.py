import argparse, os
import print_utils
import common_utils

LOGGER = print_utils.Logger()

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--input_dir', type=str, default="", help="Input files directory")
    arg_parser.add_argument('-o', '--output_dir', type=str, default="", help="Output files directory. Skip it for inplace replacement")
    arg_parser.add_argument('-t', '--tool', type=str, default="pngquant", help="Compression tool. 'pngquant' is used by default")

    args = arg_parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_dir_full_path = os.path.normpath(os.path.join(script_dir, args.input_dir))
    output_dir_full_path =  input_dir_full_path if args.output_dir == "" else os.path.normpath(os.path.join(script_dir, args.output_dir))
    LOGGER.h("%s: Compress resources %s -> %s" % (args.tool.upper(), input_dir_full_path, output_dir_full_path))
    tool_script_path = os.path.join(script_dir, "image_utils", args.tool + ".py")
    common_utils.run_py(tool_script_path, '--input_dir=' + input_dir_full_path, '--output_dir=' + output_dir_full_path)