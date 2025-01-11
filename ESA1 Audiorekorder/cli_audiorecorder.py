#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#
# Autor: Daniel Riel
# Matrikelnummer: 842 072
#
# ESA1: Audiorekorder
# Usage:
# cli_audiorecorder.py <url> [--filename=<name>] [--duration=<time>] [--blocksize=<size>]
# cli_audiorecorder.py -h | --help

# Default Webstream URL: http://live-radio02.mediahubaustralia.com/CTRW/mp3/
#
# Audio recorder.
#
# positional arguments:
# url           URL of the webstream [default: http://live-radio02.mediahubaustralia.com/CTRW/mp3/].
# fname         Name of recording [default: myRadio].
# duration      Duration of recording in seconds [default: 30].
# blocksize     Block size for read/write in bytes [default: 1024].
# options:
#   -h, --help  show this help message and exit

# requirements
# pip install argparse
# pip install requests
# pip install time
# pip install os
# import required libraries
from datetime import datetime
import argparse
import requests
import time
import os

# create command-line argument parser
parser = argparse.ArgumentParser(description='Audio recorder.')

# add arguments
#   nargs='?' means 0 or 1 arguments
#   const=1 sets the default when there are 0 arguments
parser.add_argument('url', help='URL of the webstream [default: http://live-radio02.mediahubaustralia.com/CTRW/mp3/].',
                    nargs='?', const=1, default='http://live-radio02.mediahubaustralia.com/CTRW/mp3/')
parser.add_argument(
    'fname', help='Name of recording [default: myRadio].', nargs='?', const=1, default='myRadio')
parser.add_argument(
    'duration', help='Duration of recording in seconds [default: 30].', nargs='?', const=1, default=30)
parser.add_argument(
    'blocksize', help='Block size for read/write in bytes [default: 1024].', nargs='?', const=1, default=1024)

# parse arguments from terminal
args = parser.parse_args()


def recordStream():
    ''' function record audio '''

    # access arguments
    start_time = (datetime.utcnow()-datetime.fromtimestamp(0)
                  ).total_seconds()                             # get current system time stamp
    duration = int(args.duration)
    url = requests.get(args.url, stream=True)

    os.system('cls')                                            # clear screen

    print('Aufnahme gestartet..')

    with open(args.fname + '.mp3', 'wb') as file:               # write the stream to .mp3 file
        try:
            while ((datetime.utcnow()-datetime.fromtimestamp(0)).total_seconds()-start_time) < duration:
                for block in url.iter_content(int(args.blocksize)):
                    file.write(block)

                    # command-line indicator
                    print('*', flush=True, end='\r')
                    time.sleep(0.2)
                    print(' ', flush=True, end='\r')
                    time.sleep(0.2)

                    if duration == 0:
                        break

                    duration -= 1
        except KeyboardInterrupt:
            print("Die Aufnahme wurde durch ein Keyboard interrupt beendet!")

    print('Aufnahme beendet!')


def savedStreams():
    '''Anzeige aller gespeicherten Streams'''
    # get current directory
    currentDirectory = '.'
    dir_path = os.path.dirname(os.path.realpath(__file__))

    print('Current Directory: ' + dir_path)
    print('\nDirectory Files:')

    for path, dirs, files in os.walk(currentDirectory):
        for filename in files:
            if filename.lower().endswith('.mp3'):               # filter by .mp3
                print(os.path.join(path, filename))


# function call
recordStream()
savedStreams()