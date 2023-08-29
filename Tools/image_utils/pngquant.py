import os, sys
import imgcompressor
import argparse

class pngquant_compressor(imgcompressor.IMGCompressor):
    def __init__(self):
            imgcompressor.IMGCompressor.__init__(self, "PNGQUANT")

    def get_command_line_win( self, input_file, output_file, params ):
        self.safe_copy_file(input_file, output_file)
        command_line = "%s \"%s\" %s" % (os.path.join(self.script_dir, "pngquant/Win/pngquant.exe"), output_file, params)
        return command_line
    
    def get_command_line_osx( self, input_file, output_file, params ):
        self.safe_copy_file(input_file, output_file)
        command_line = "'%s' '%s' %s" % (os.path.join(self.script_dir, "pngquant/MacOS/pngquant"), output_file, params)
        return command_line

    def get_command_line_linux( self, input_file, output_file, params ):
        self.safe_copy_file(input_file, output_file)
        command_line = "'%s' '%s' %s" % ("pngquant", output_file, params)
        return command_line

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '-i', type=str, help='Input directory')
    parser.add_argument('--output_dir', '-o', type=str, default="", help='Output directory')
    parser.add_argument('--params', '-p', type=str, default="--force --ext=.png --quality=0-100 --speed=1", help='Compression parameters')
    args = parser.parse_args()

    compressor = pngquant_compressor()
    compressor.compress(args.input_dir, args.output_dir, args.params, ["*.png"])
