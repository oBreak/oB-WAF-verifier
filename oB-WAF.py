#!/usr/bin/env python

'''
Written by oBreak.

Disclaimer: This tool should not be referenced in legal proceedings.

Source code should be found at https://github.com/oBreak/oB-WAF-verifier
'''

# Imports

import requests
import urllib.request
import time
from pathlib import Path
import os
from os import listdir
import configparser
import texttable

# Global vars

debug           = ['***********','Begin debug log','***********']
out             = []
iF              = []
siteTups        = []
sites           = []
testCases       = []
fullOut         = [['Website','Search terms','Match']]

# Taken from recon

debugSet        = True
debugLog        = []
home            = str(Path.home())
fileDir         = os.path.dirname(os.path.realpath('__file__'))
outfileMac      = os.path.join(fileDir, 'out/out.txt')
outfile         = os.path.join(fileDir, 'out/out.txt')
debugfileMac    = os.path.join(fileDir, 'debug/debug.txt')
debugfile       = os.path.join(fileDir, 'debug/debug.txt')
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

fileCount       = int(0)
conf            = {}
lineBreaks      = str('\n')
scanresults     = []
totalsitesAndScans = int(0)
percentageComplete = int(0)




# Functions

'''
inbound() is intended to review all files from the relative /in/ directory that are of type ".txt", ".log", or ".csv".
These files are added to the inbound file list (variable iF). If files are outside of specified file types, it
does not add them to the inbound file list. Inbound file list is then returned by the function.
'''

def inbound():
    debug.append('\tinbound() start: checking /in/ folder for files containing sites to which we will connect')
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
        debug.append('\t\tiF (inbound files) contains:')
        for x in iF:
            debug.append('\t\t' + x + ' added to inbound files list variable (iF)')
        debug.append('\t\tfileCount is: ' + str(fileCount))
    debug.append('\tinbound() end')
    return iF


def readConf():
    debug.append('\treadConf() start: reading configuration file for search terms')
    global conf
    conf = configparser.ConfigParser()
    conf.read('conf/conf.ini')
    if debugSet == True:
        debug.append('\t\tConfiguration sections loaded:')
        for i in conf.sections():
            debug.append('\t\t\t' + str(conf[i]))
    debug.append('\treadConf() end')
    return



'''
parse() is intended to pull the websites from files in the inbound file list (iF), which is created in inbound(), 
and adds them to the sites list. This is accomplished by putting the "line" from the file into a tuple in the
webs variable. Then the webs first tuple portion is added to the site list.

Ex:

webs = ('https://www.example.com', <blank>)
sites = ['https://www.example.com']

The sites list is a global variable that is used by the scrape() function.
'''
def parse(iF):
    debug.append('\tparse() start: extracting sites to connect to from files in the /in/ folder')
    file = open('in/' + iF, 'r')
    for line in file:
        # line is http address
        # Reset webs to empty tuple
        webs = ()
        # print(line + ' in file ' + iF)
        line = line.strip()  # Removes blank lines.
        if line:
            ''' This portion of the script is meant to discover if the inbound files are correctly formatted.
            Decision tree:
                If IP -> Add IP to sites list (in other languages, this is an array)
                If CIDR -> Convert to IPs
                    -> Add all IPs to sites list
                If IP Range -> Convert to IPs
                    -> Add all IPs to sites list


            if line == IP address format:
                sites.append(line)
                if debugSet == True:
                debugLog.append('Appending ' + line + ' to sites.')
            '''
            webs = (line,)
            sites.append(webs[0])
            if debugSet == True:
                debug.append('\t\tAppending ' + webs[0] + ' to sites.')
    debug.append('\tparse() end')
    pass

'''
scrape() is intended to get the response.text from each of the sites identified in the parse() function.

It checks the length of the 'sites' list. Then, for each site in the list, it will try a get request for the
site. This get request is then appended to the 'out' list for output into the /out/ folder in the webout() function.

Additionally, the response.text is also appended to the 'siteTups' list as a tuple with...

[('https://www.example.com/', 'Output of response.text'), ('https://www.example2.com/', 'Output of response.text'), ...]

'''
def scrape():
    debug.append('\tscrape() start: sending get requests to sites')
    global out
    global siteTups
    global testCases # New stuff

    # Take sites tuple which is now (site address, <none>) and use requests to get the text version of the site.

    sitecount = len(sites)
    # print(sitecount)

    for i in range(0,(sitecount)):
        try:
            response = requests.get(sites[i])
        except:
            debug.append('\t\tError with requests in scrape()')
        try:
            debug.append('\t\tStatus code of scrape on site ' + sites[i] + ' is: ' + str(response.status_code))
            if response.status_code == 200:
                debug.append('\t\tConnection successful.')
        except:
            debug.append('\t\tError getting status code of site: ' + sites[i])
        r = response.text
        siteTups.append((sites[i],r))
    debug.append('\tscrape() end')

    return

'''
passfail() is intended to check whether criteria set in the configuration file matches any of the response.text of the
get request that was obtained in scrape().

It searches...
    First term -> check site 1, check site 2, etc.
    Second term -> check site 1, check site 2, etc.

It checks for terms defined in the 'terms' section of the config, ignoring other parts of the config.
'''

def passfail():
    sitecount = len(sites)
    debug.append('\tpassfail() start: checking for term matches against web response')
    global siteTups
    global fullOut
    termcount = 0
    for i in range(0, (sitecount)):   # New stuff to put results in list of lists.
        try:
            testCases.append([sites[i]])
            #testCases[i].append('pass/fail')
        except IndexError:
            debug.append('\t\tIndex error in scrape during testCases append.')
            pass

    for j in conf['terms']:
        debug.append('\t\tIterating term: ' + j )
        termcount = termcount + 1
        criteria = conf['terms'][j]

        # Not pretty version (leaving this in here for legacy purposes); note this doesn't even need to be siteTups
        # which is only here because I hadn't created list for fullOut.

        # for i in siteTups:
        #     debug.append('\t\t\tIterating site: ' + i[0])
        #     if i[1].find(criteria) != -1:
        #         out.append("Site " + i[0] + " *matches* criteria #" + str(termcount) + ": " + criteria)
        #     else:
        #         out.append("Site " + i[0] + " does not match search criteria #" + str(termcount) + ": " + criteria)

    # New stuff! Doesn't work yet.
    sitenum = int(0)
    for x in testCases: #iterates through sites, starting at index [0]
        item1 = x
        termcount = 0
        for j in conf['terms']: #iterates through terms
            termcount = termcount + 1 #iterates next term for each loop, starting at 1
            # compare site results to terms
            item2 = j

            # return pass/fail value
            '''
            testCases is [
            '''
            criteria = conf['terms'][j]
            # print(sitenum)
            if sites[sitenum].find(criteria) != -1:
                # print("Site " + x[0] + " *matches* criteria #" + str(termcount) + ": " + criteria)
                fullOut.append([x[0], criteria, 'True'])
            else:
                # print("Site " + x[0] + " does not match search criteria #" + str(termcount) + ": " + criteria)
                fullOut.append([x[0], criteria, 'False'])
            # store list entry with list [site, term, pf value]

        sitenum = sitenum + 1



    return

'''
prettyOut() is intended to output easy to read text representative of the results. It uses texttable
to format the output.

Supposed to look like...

Site 1    Term 1       Yes/no
Site 1    Term 2       Yes/no
Site 2    Term 1       Yes/no

Data is in fullOut table of tables which is populated in pass/fail.
'''

def prettyOut():
    debug.append('\tprettyOut() start: outputting fancy, readable table to out file.')
    xtable = texttable.Texttable()
    xtable.add_rows(fullOut)
    out.append(xtable.draw())
    debug.append('\tpassfail() end')


'''
siteinfo() is appending the website response.text output to the 'out'. This was originally in the parse()
function but doesn't really belong there. Since parse needs to run, it breaks the ability to shift where 
the output shows up in the output log. Since the point of the program is to determine pass/fail checks,
the first part of the output shouldn't be a bunch of information that doesn't deliver the point.

This information is still important for determining the text that you want to view, but should be after
the pass fails.

Also added some formatting so it is easier to read/decipher in the out text.
'''

def siteinfo():
    debug.append('\tsiteinfo() start: sending site info to out list')
    sitecount = len(sites)
    for i in range(0,(sitecount)):
        out.append('\n\n\n')
        out.append('*' * 40)
        out.append('For site: ' + siteTups[i][0])
        out.append('*' * 40)
        out.append(siteTups[i][1])
        out.append('\n\n\n')
    debug.append('\tsiteinfo() end')
    return

'''
webout() is intended to print the response.text from each of the sites identified to an out file in the 
relative /out/ folder.
'''

def webout():
    debug.append('\twebout() start: printing to file for output')
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
        f.write(j)
        f.write(lineBreaks)  # This is to add a new line at the end of each line of the log or text file.
        n = n + 1
        if n % 100 == 0:
            print('\tWriting outputs: ' + str(n) + ' list items complete.')
        else:
            pass
    else:
        pass
    print('\tOutput complete: ' + str(n) + ' list items written.\n')
    debug.append('\twebout() end')
    return

'''
debugout() is intended to print the debug log for the program.
The debug list variable contains all log entries.
This might be a candidate for concurrent processing, as it won't complete if the program breaks midway.
'''

def debugout():
    debug.append('\tdebugout() start: printing debug to file.')
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
        f.write(j)
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

'''
main() is the main program. Workflow is:

- Get list of files with sites to review
- Extract sites from list of files
- For each site in sites, requests from the sites and adds to sites and siteTups lists
- Reads configuration file.
- Checks against search criteria contained in configuration file; adds pass/fail results to out list.
- Adds output from site response to out list.
- Print debug log to debug file.
- Print out list to out file.
- End.
'''

def main():
    debug.append('main() start')
    iF = inbound()
    for t in iF:
        parse(t)
    scrape()
    readConf()
    passfail()
    prettyOut()
    siteinfo()
    webout()
    debug.append('main() end')
    if debugSet == True:
        debugout()
    return

# Running the program

main()
