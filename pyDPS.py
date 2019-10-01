#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# import modules
import sys, getopt, os

# import modules from file modules.py
from modules import (devicePath, rdserialCmd, 
                     deviceOn, deviceOff, 
                     setVolt, setAmps, 
                     runSubprocess, onError, usage)

# handle options and arguments passed to script
try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 '10'
                                 'V:A:g:'
                                 'vh',
                                 ['on', 'off', 'volt=', 'ampere=', 'group=', 
                                  'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

# if no options passed, then exit
if len(sys.argv) == 1:  # no options passed
    onError(2, "No options given")
    
on = False
off = False

group = 0
volt = 0
ampere = 0

verbose = False
    
    
    
# interpret options and arguments
for option, argument in myopts:
    if option in ('-1', '--on'):  # verbose output
        on = True
    elif option in ('-0', '--off'):  # verbose output
        off = True
    elif option in ('-V', '--volt'):  # verbose output
        volt = argument
    elif option in ('-A', '--ampere'):  # verbose output
        ampere = argument
    elif option in ('-g', '--group'):  # verbose output
        group = argument
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
        onError(6, "Group must be a number between 0 and 8")

cmd = rdserialCmd
cmd = cmd + " --group " + str(group)

if volt:
    cmd = cmd + setVolt(rdserialCmd, group, volt, verbose)
    
if ampere:
    cmd = cmd + setAmps(rdserialCmd, group, ampere, verbose)
     
if on:
    cmd = cmd + deviceOn(rdserialCmd, verbose)
    
if off:
    cmd = cmd + deviceOff(rdserialCmd, verbose)
    
    
# check if device exists
if not os.path.isfile(devicePath):
    onError(7, "Device '" + devicePath + "' does not exist")
    
if verbose:
    cmd = cmd + " --debug"
    
runSubprocess(cmd, verbose)


    