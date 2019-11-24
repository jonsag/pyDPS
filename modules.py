#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import configparser, os, sys, subprocess

config = configparser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

# read variables from config file
devicePath = config.get('device', 'devicePath').strip()

rdserialCmd = "rdserialtool --serial-device " + devicePath + " dps"

# handle errors
def onError(errorCode, extra):
    print("\nError " + str(errorCode) + ":")
    if errorCode in (1, 2): # print error information, print usage and exit
        print(extra)
        usage(errorCode)
    elif errorCode in (3, 5, 6, 7, 8, 9): # print error information and exit
        print(extra)
        sys.exit(errorCode)
    elif errorCode == 4: # print error information and return running program
        print(extra)
        return
        
# print usage information        
def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    
    print("%s -1/-0" % sys.argv[0])
    print("    Turn device on/off")
    
    print("\n%s -V [volts] (-g [group])" % sys.argv[0])
    print("    Set output voltage to [volts] (for group no [group])")
    
    print("\n%s -A [amperes] (-g [group])" % sys.argv[0])
    print("    Set max current to [amperes] (for group no [group])")
    
    print("\n%s -l -g [group]" % sys.argv[0])
    print("    Load group no [group]")
    
    print("\n%s -s" % sys.argv[0])
    print("    Show device status")
    
    print("\n%s -v" % sys.argv[0])
    print("    Verbose output")
    
    print("\n%s -h" % sys.argv[0])
    print("    Show help")
    
    #print("\nrdserialtool dps --help")
    #print("----------------------------------------")
    #runSubprocess("which rdserialtool", False)
    #print()
    #runSubprocess("rdserialtool dps --help", False)
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

def runSubprocessCapture(cmd, verbose):
    if verbose:
        print("\n--- Running subprocess")
        print("    Constructing command from \n    " + cmd + " ...")
        
    cmdList = cmd.split()
    
    if verbose:
        print("    Command list: \n        " + str(cmdList))
    
    process = subprocess.Popen(cmdList, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
        
    return stdout
    
def deviceOn(verbose):
    if verbose:
        print("\n--- Turning device ON ...")
    return " --set-output-state on"
    
def deviceOff(verbose):
    if verbose:
        print("\n--- Turning device OFF ...")
    return " --set-output-state off"
    
def setVolt(group, volt, verbose):
    if verbose:
        print("\n--- Setting volt to " + str(volt) + "V for group " + str(group))
    return " --set-group-volts " + str(volt)
    
def setAmps(group, ampere, verbose):
    if verbose:
        print("\n--- Setting current to " + str(ampere) + "A for group " + str(group))
    return " --set-group-amps " + str(ampere)

def useGroup(group, verbose):
    if verbose:
        print("\n--- Loading group no " + str(group))
    return " --load-group " + str(group)

def groupSettings(verbose):
    if verbose:
        print("\n--- Getting group settings ...")
        
    cmd = rdserialCmd + " --all-groups"
    
    output = runSubprocessCapture(cmd, verbose)
        
    return output
    
    
    
    
    
    
    
    
    
    
    
