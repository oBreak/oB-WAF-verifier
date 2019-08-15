#!/usr/bin/env python

'''
Written by oBreak.

Disclaimer: This tool should not be referenced in legal proceedings.
'''

# Imports

import requests
import urllib.request
import time

# Global vars

debug = ['***********','Begin debug log']

# Functions

def scrape():
    urls = ['http://www.google.com', 'https://www.example.com']
    try:
        response = requests.get(urls[0])
    except:
        debug.append('\t\tError with requests in scrape()')
        return
    print(response.status_code)
    print(response.text)
    debug.append('\tscrape() end')
    return

def debugout():
    lineBreaks = '\n'
    n=0

    # Set time for out file naming
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Designate debug file
    debugfile = 'debug/debug-' + timestr + '.log'
    print(debugfile + ' created.')

    # Open debug file
    try:
        f = open(debugfile, 'w')
        print('')
        print('\tSetting debug file,', debugfile)
        print('')
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
    print('\tOutput complete: ' + str(n) + ' lines written.')
    print('\n')
    return


    return

def main():
    debug.append('main() start')
    debug.append('\tscrape() start')
    scrape()
    debug.append('main() end')
    debugout()
    return

main()


# debug()
