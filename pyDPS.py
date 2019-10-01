#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# import modules
import sys, getopt, os

# import modules from file modules.py
from modules import (devicePath, rdserialCmd, 
                     deviceOn, deviceOff, 
                     setVolt, setAmps, useGroup, 
                     groupSettings, 
                     runSubprocess, onError, usage)

# handle options and arguments passed to script
try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 '10ls'
                                 'V:A:g:'
                                 'vh',
                                 ['on', 'off', 'load', 'status', 
                                  'volt=', 'ampere=', 'group=', 
                                  'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

# if no options passed, then exit
if len(sys.argv) == 1:  # no options passed
    onError(2, "No options given")
    
on = False
off = False

loadGroup = False
status = False

group = 0
volt = 0
ampere = 0

verbose = False
    
    
    
# interpret options and arguments
for option, argument in myopts:
    if option in ('-1', '--on'):  # set device ON
        on = True
    elif option in ('-0', '--off'):  # set device OFF
        off = True
    elif option in ('-V', '--volt'):  # set V
        volt = argument
    elif option in ('-A', '--ampere'):  # set A
        ampere = argument
    elif option in ('-g', '--group'):  # use group no 
        group = argument
    elif option in ('-l', '--load'):  # load group
        loadGroup = True
    elif option in ('-s', '--status'):  # load group
        status = True
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)

if on and off:
    onError(3, "Both 'on' and 'off' can't be set")

try:
    group = int(group)
except:
    onError(5, "Group argument must be an integer")
else:
    if group < 0 or group > 9:
        onError(6, "Group must be a number between 0 and 9")

if loadGroup and volt:
    onError(8, "You can't set both 'load' and 'volt'")
elif loadGroup and ampere:
    onError(9, "You can't set both 'load' and 'ampere'")

cmd = rdserialCmd
cmd = cmd + " --group " + str(group)

if off:
    cmd = cmd + deviceOff(verbose)
else:
    if status:
        output = groupSettings(verbose)
        
        output = output.split("\n")
        
        for line in output:
            print(line)
        
        sys.exit(0)
        
    if on:
        cmd = cmd + deviceOn(verbose)
        
    if volt:
        cmd = cmd + setVolt(group, volt, verbose)
        
    if ampere:
        cmd = cmd + setAmps(group, ampere, verbose)
    
    if loadGroup:
        cmd = cmd + useGroup(group, verbose)
    

# check if device exists
if os.system("ls " + devicePath) != 0:
    onError(7, "Device '" + devicePath + "' does not exist")
    
#if verbose:
#    cmd = cmd + " --debug"
    
runSubprocess(cmd, verbose)


    
