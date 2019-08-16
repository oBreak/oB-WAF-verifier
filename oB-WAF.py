#!/usr/bin/env python

'''
Written by oBreak.

Disclaimer: This tool should not be referenced in legal proceedings.
'''

# Imports

import requests
import urllib.request
import time
from pathlib import Path
import os
from os import listdir

# Global vars

debug = ['***********','Begin debug log']
out = []
iF = []

# Taken from recon

debugSet        = True
debugLog        = []
home            = str(Path.home())
fileDir         = os.path.dirname(os.path.realpath('__file__'))
outfileMac      = os.path.join(fileDir, 'out/out.txt')
outfile         = os.path.join(fileDir, 'out/out.txt')
debugfileMac    = os.path.join(fileDir, 'debug/debug.txt')
debugfile       = os.path.join(fileDir, 'debug/debug.txt')
scansrc         = os.path.join(fileDir, 'scansrc/')
mypath          = ''
mypathMac       = home + "/Projects/gh-oB-WAF-verifier/in/"

# Checking for if the OS is Windows or Linux

osCheck         = ''
isWin           = 0

# Windows Paths

debugfileWin    = os.path.join(fileDir, 'debug\\debug.txt')
# mypathWin       = home + "\\Projects\\gh-oB-WAF-verifier\\in\\"
mypathWin       = home + "\\Projects\\gh-oB-WAF-Verifier\\in\\"
outfileWin      = os.path.join(fileDir, 'out\\out.txt')

targets         = []
fileCount       = int(0)
conf            = {}
lineBreaks      = str('\n')
scanresults     = []
totalTargetsAndScans = int(0)
percentageComplete = int(0)




# Functions

def inbound():
    global fileCount, mypath
    iF = []   # iF is inbound files
    try:
        for f in listdir(mypathWin):
            if f.find(".txt", len(f) - 4) != -1:
                iF.append(f)
            elif f.find(".log", len(f) - 4) != -1:
                iF.append(f)
            elif f.find(".csv", len(f) - 4) != -1:
                iF.append(f)
            else:
                #print(f + ' outside of txt, log, or csv types.')
                fileCount = fileCount - 1
            fileCount = fileCount + 1
            print (range(fileCount))
        mypath = mypathWin
    except FileNotFoundError:
        for f in listdir(mypathMac):
            if f.find(".txt", len(f) - 4) != -1:
                iF.append(f)
            elif f.find(".log", len(f) - 4) != -1:
                iF.append(f)
            elif f.find(".csv", len(f) - 4) != -1:
                iF.append(f)
            else:
                #print(f + ' outside of txt, log, or csv types.')
                fileCount = fileCount - 1
            fileCount = fileCount + 1
        mypath = mypathMac
    if debugSet == True:
        debugLog.append('iF (inbound files) contains:')
        for x in iF:
            debugLog.append(x + ' added to iF')
        debugLog.append('fileCount is: ' + str(fileCount))
    # for t in iF:
    #     print(t, "in inbound()")
    return iF


def parse(x):
    file = open('in/' + x, 'r')
    for line in file:
        line = line.strip()  # Removes blank lines.
        if line:
            ''' This portion of the script is meant to discover if the inbound files are correctly formatted.
            Decision tree:
                If IP -> Add IP to target list (in other languages, this is an array)
                If CIDR -> Convert to IPs
                    -> Add all IPs to targets list
                If IP Range -> Convert to IPs
                    -> Add all IPs to targets list


            if line == IP address format:
                targets.append(line)
                if debugSet == True:
                debugLog.append('Appending ' + line + ' to targets.')
            '''
            targets.append(line)
            if debugSet == True:
                debugLog.append('Appending ' + line + ' to targets.')
    pass


def scrape(iF):
    global out
    #urls = ['http://www.google.com', 'https://www.espn.com']
    for t in targets:
        # print(t)
        try:
            response = requests.get(t)
        except:
            debug.append('\t\tError with requests in scrape()')
            return
    # print(response.status_code)
    # print(response.text)
    out.append(response.text)
    debug.append('\tscrape() end')
    return


def webout():
    # Set local variables
    lineBreaks = '\n'        # This is making sure the outfile has separate lines.
    n=0                      # Variable for counting lines written to debug.

    # Set time for out file naming
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Designate out file
    outfile = 'out/out-' + timestr + '.log'
    print(outfile + ' created.')

    # Open debug file
    try:
        f = open(outfile, 'w')
        print('\n\tSetting out file,', outfile, ' \n')
    except:
        print("\tFailed to open out file!")
        f.close()

    # Write out file
    for j in out:
        f.write(str(j))
        f.write(lineBreaks)  # This is to add a new line at the end of each line of the log or text file.
        n = n + 1
        if n % 100 == 0:
            print('\tWriting outputs: ' + str(n) + ' lines complete.')
        else:
            pass
    else:
        pass
    print('\tOutput complete: ' + str(n) + ' lines written.\n')
    return

def debugout():
    # Set local variables
    lineBreaks = '\n'        # This is making sure the outfile has separate lines.
    n=0                      # Variable for counting lines written to debug.

    # Set time for debug file naming
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Designate debug file
    debugfile = 'debug/debug-' + timestr + '.log'
    print(debugfile + ' created.')

    # Open debug file
    try:
        f = open(debugfile, 'w')
        print('\n\tSetting debug file,', debugfile, ' \n')
    except:
        print("\tFailed to open debug file!")
        f.close()

    # Write debug file
    for j in debug:
        f.write(str(j))
        f.write(lineBreaks)  # This is to add a new line at the end of each line of the log or text file.
        n = n + 1
        if n % 100 == 0:
            print('\tWriting outputs: ' + str(n) + ' lines complete.')
        else:
            pass
    else:
        pass
    print('\tOutput complete: ' + str(n) + ' lines written.\n')
    return


def main():
    debug.append('main() start')
    debug.append('\tinbound() start')
    iF = inbound()
    # for i in iF:
    #     print(i)
    debug.append('\tinbound() end')
    debug.append('\tparse() start')
    for t in iF:
        parse(t)
    debug.append('\tparse() end')
    debug.append('\tscrape() start')
    for t in targets:
        scrape(t)
    debug.append('\tscrape() end')
    debug.append('main() end')
    debugout()
    webout()
    return

main()


# debug()
