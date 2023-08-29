import os, sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ColoredString:
    def __init__(self, string, color):
        self.string = string
        self.color = color

    def __repr__(self):
        return self.color + self.string + bcolors.ENDC

class Logger:
    def __init__(self):
        self.error_color = bcolors.FAIL
        self.warning_color = bcolors.HEADER
        self.errors = []
        self.warnings = []

    def e(self, message, padding=0, saveMessage=True):
        print(ColoredString(padding * ' ' + "ERROR: " + message, bcolors.BOLD + self.error_color))
        if saveMessage:
            self.errors.append(message)

    def i(self, message, padding=0, color = bcolors.OKBLUE):
        print(ColoredString(padding * ' ' + "INFO: " + message, color))

    def w(self, message, padding=0, saveMessage=True):
        print(ColoredString(padding * ' ' + "WARNING: " + message, bcolors.BOLD + self.warning_color))
        if saveMessage:
            self.warnings.append(message)

    def h(slef, message, padding=0):
        print(ColoredString(padding * '-' + message, bcolors.BOLD))
    
    def __del__(self):
        title = 50*'-' + "LOGS DUMP" + 50*'-'
        self.h(title)
        for message in self.warnings:
            self.w(message, 4, False)
        for message in self.errors:
            self.e(message, 4, False)
        print(ColoredString(len(title)*'-' + 2*'\n', bcolors.OKGREEN + bcolors.BOLD))
