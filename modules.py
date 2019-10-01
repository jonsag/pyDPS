#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os, sys, subprocess

config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# read variables from config file
var = config.get('header', 'var').strip()

# handle errors
def onError(errorCode, extra):
    print("\nError:")
    if errorCode in (1, 2): # print error information, print usage and exit
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
    
    print("\n%s -v" % sys.argv[0])
    print("    Verbose output")
    
    print("\n%s -h" % sys.argv[0])
    print("    Show help")
    
    print("\nrdserialtool dps --help")
    print("----------------------------------------")
    runSubprocess("which rdserialtool", False)
    print()
    runSubprocess("rdserialtool dps --help", False)
    sys.exit(exitCode)
    
def runSubprocess(cmd, verbose):
    if verbose:
        print("\n--- Running subprocess")
        print("    Constructing command from \n    " + cmd + " ...")
        
    cmdList = cmd.split()
    
    if verbose:
        print("    Command list: \n        " + str(cmdList))
                
    #print("\n" + cmdList[0] + " session starts\n----------")
    response = subprocess.run(cmdList)
    #print("----------\n" + cmdList[0] + " session ended")
    
    returnCode = response.returncode
    if returnCode != 0:
        print("\nProcess exited uncleanly\nwith exit code " + str(response.returncode))
    

    
    
    
    
    
    
    
    
    
    
    
    
    