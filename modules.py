#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os, sys

config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# read variables from config file
var = config.get('header', 'var').strip()

# handle errors
def onError(errorCode, extra):
    print("\nError:")
    if errorCode in(1, 2): # print error information, print usage and exit
        print(extra)
        usage(errorCode)
    elif errorCode == 3: # print error information and exit
        print(extra)
        sys.exit(errorCode)
    elif errorCode == 4: # print error information and return running program
        print(extra)
        return
        
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s " % sys.argv[0])

    sys.exit(exitCode)