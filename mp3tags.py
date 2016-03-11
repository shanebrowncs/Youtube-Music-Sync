#!/usr/bin/env python

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Author: Shane 'SajeOne' Brown
# Date: 11/03/2016
# Revision: 2 - Added argparse and PATH option
# Description: Automatically adds ID3 tags to songs based on '-' delimiter
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

import os
import os.path
import subprocess
import argparse

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError

# Setup Arguments
parser = argparse.ArgumentParser(prog='mp3tags')
parser.add_argument("-p", "--path", help="Path to directory with files to tag, defaults to CWD")
args = parser.parse_args()

# Parse possible passed Path into 'path' var
path = ""
if args.path:
    path = args.path
else:
    path = os.getcwd()


# Get files in PATH directory
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

# Adds artist and title tags to file at fileName
def tagFile(fileName, title, artist):
    try:
        audio = EasyID3(fileName)
        audio['title'] = title
        audio['artist'] = artist
        audio.save()
        return True
    except ID3NoHeaderError:
        return False 

# START EXECUTION

# Loop through all files and split artist - title for tagging; tag file
for myFile in files:
    splitSong = myFile.split('-')
    if len(splitSong) >= 2:
        if tagFile(path + "/" + myFile, splitSong[1].strip(), splitSong[0].strip()):
            print("Tagged " + myFile)
        else:
            print("No ID3 Header on " + myFile)
    else:
        print("No Dilimeter for " + myFile)
