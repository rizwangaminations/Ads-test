import os, sys
import platform
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import print_utils, Helper
from fnmatch import fnmatch
import shutil
import argparse
from subprocess import Popen, PIPE

class IMGCompressor:
    def __init__(self, name):
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.name = name.upper()
        self.logger = print_utils.Logger()
        self.input_size_bytes = 0
        self.output_size_bytes = 0

    def __del__(self):
        profit_in_bytes = self.input_size_bytes - self.output_size_bytes
        marker_color = print_utils.bcolors.FAIL if profit_in_bytes < 0 else print_utils.bcolors.OKGREEN       
        self.logger.h("----%s DONE (%s%i bytes -> %i bytes%s)-----" % (self.name, marker_color, self.input_size_bytes, self.output_size_bytes, print_utils.bcolors.ENDC + print_utils.bcolors.BOLD))

    def safe_copy_file( self, src_file, dest_file ):
        if os.path.normpath(src_file) == os.path.normpath(dest_file):
            return
        dest_dir = os.path.dirname( dest_file )
        #check and create output directory
        Helper.checkCreateDir(dest_dir)
        shutil.copy(src_file, dest_file)
    
    def compress_file(self, input_file, output_file, params):
        old_size = os.path.getsize(input_file)
        command_line = ""
        if platform.system() == "Windows":
            command_line = self.get_command_line_win(input_file, output_file, params)
        elif platform.system() == "Darwin":
            command_line = self.get_command_line_osx(input_file, output_file, params)
        elif platform.system() == "Linux":
            command_line = self.get_command_line_linux(input_file, output_file, params)
        #if command_line is invalid -> inform and return
        if command_line == "":
            self.logger.e("not compress command specified for current platform")
            raise Exception("not compress command specified for current platform")
            return
        #check create dir for output file
        Helper.checkCreateDir(os.path.dirname(output_file))
        ret = self.execute_command( command_line )
        if ret != 0:
            self.logger.w("FAILED with %i. Copying %s --> %s\nCommand line: %s" % (ret, input_file, output_file, command_line))
            self.safe_copy_file(input_file, output_file)
        else:
            new_size = os.path.getsize(output_file)
            self.input_size_bytes += old_size
            self.output_size_bytes += new_size
            profit_in_bytes = old_size - new_size
            marker_color = print_utils.bcolors.FAIL if profit_in_bytes < 0 else print_utils.bcolors.OKGREEN   
            self.logger.i("COMPRESSED (%s%i -> %i = %i bytes%s) %s --> %s" % (marker_color, old_size, new_size, profit_in_bytes, print_utils.bcolors.OKBLUE, input_file, output_file) )
            pass

    def execute_command( self, command ):
        ret = 0
        try:
            proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
            out, err = proc.communicate()
            exitcode = proc.returncode
            self.logger.w("Command executed correctly, output:%s, error:%s" % (out, err))
            return exitcode;
        except Exception as e: 
            self.logger.w("Error executing command %s %s %s" % (self.name, command, e))
            ret = 1
        return ret
    

    def get_command_line_win( self, input_file, output_file, params ):
        return "Win commandLine"

    def get_command_line_osx( self, input_file, output_file, params ):
        return "OSX commandLine"

    def get_command_line_linux( self, input_file, output_file, params ):
        return "Linux commandLine"

    def compress( self, input_dir, output_dir, params, extensions = ["*.png"] ):
        if output_dir is None or output_dir == "":
            output_dir = input_dir
        copy_not_images = ( os.path.normpath(input_dir) != os.path.normpath(output_dir) )
        self.logger.i("COMPRESSING DIRECTORY %s --> %s " % (input_dir, output_dir))
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                input_file = os.path.join(root, file)
                output_file = input_file.replace(input_dir, output_dir)
                if any( fnmatch(file, ext) for ext in extensions ):
                    #compressing image
                    self.compress_file( input_file, output_file, params )
                elif copy_not_images == True:
                    #just copying file
                    self.safe_copy_file(input_file, output_file)