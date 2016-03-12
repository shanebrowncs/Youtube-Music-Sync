#!/usr/bin/env python

import json
from pprint import pprint
import urllib.request as REQ
import subprocess as sp
import os
from os.path import isfile, join
import sys
import argparse
import re

def loadConfigFile():
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + "/config.json", "r") as configFile:
            data = configFile.read()
            jsonObj = json.loads(data)
            return jsonObj
    except (FileNotFoundError, IOError) as e:
        return False

def writeDefaultConfig():
    xdgConfig = os.getenv('XDG_CONFIG_HOME')
    configList = {'playlistID': 'PLP37tSKMt8KzgfdABgSZQ2wV2IirbTOPR', 'googleAPIKey': 'PUT KEY HERE', 'destination': '/home/shane/Music'}

    jsonSaveFile = json.dumps(configList, indent=4)
    with open(os.path.dirname(os.path.realpath(__file__)) + "/config.json", "w") as configFile:
        print(jsonSaveFile, file=configFile)

def downloadVideo(url, path):
    proc = sp.Popen(['youtube-dl', '--extract-audio', '--audio-format', 'mp3', '--output', path + "/%(title)s.%(ext)s", url], stdout=sp.PIPE)
    result = proc.communicate()[0]
    status = proc.returncode
    

    if status == 0:
        return True

    return False

def downloadPage(url):
    response = REQ.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    return text

def decodeJson(encodedJson):
    data = json.loads(encodedJson)
    return data

def convertListFileSystemNeutral(convList):
    for index, value in enumerate(convList):
        convList[index] = re.sub('[^A-Za-z0-9]+', '', os.path.splitext(convList[index])[0])

    return convList

def convertStringFileSystemNeutral(song):
    song = re.sub('[^A-Za-z0-9]+', '', os.path.splitext(song)[0])
    return song

def getSongList(path):
    songs = [f for f in os.listdir(path) if isfile(join(path, f))]
    return songs

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--id3tag', help="Automatically sets up ID3 tags based on '-' delimiter. Requires optional dependency 'python-mutagen'", action="store_true")
    parser.add_argument('-v', '--verbose', help="Includes skipped songs(Already downloaded and in active playlist)", action="store_true")
    parser.add_argument('-s', '--simulate', help="Simulates without actually downloading, good for speed testing", action="store_true")
    args = parser.parse_args()
    return args


# BEGIN EXECUTION

## Handle Arguments
args = parseArguments()

tagFiles = False
verbose = False
simulate = False

if args.id3tag:
   tagFiles = True

if args.verbose:
    verbose = True

if args.simulate:
    simulate = True


## Handle Configuration
config = loadConfigFile()

if not config:
    writeDefaultConfig()
    print("No config, wrote default. Ensure to edit appropriately")
    sys.exit(1)

url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=" + config['playlistID'] + "&key=" + config['googleAPIKey'] + "&maxResults=50"


## Download page and decode data
page = downloadPage(url)
jsonData = decodeJson(page)

songs = getSongList(config['destination'])
songs = convertListFileSystemNeutral(songs)

curSongList = []


## Loop through items and compare repos
for items in jsonData['items']:
    neutralCmp = convertStringFileSystemNeutral(items['snippet']['title']) 
    curSongList.append(neutralCmp)
    if not neutralCmp in songs:
        print("Downloading " + items['snippet']['title'] + "..")
        if simulate or downloadVideo("https://youtube.com/watch?v=" + items['snippet']['resourceId']['videoId'], config['destination']):
            songs.append(items['snippet']['title'])
        else:
            print("\n--DOWNLOAD FAILED--\n")
    else:
        if verbose:
            print("SKIPPING " + items['snippet']['title'])


## Delete songs removed from remote
songs = getSongList(config['destination'])
songs = convertListFileSystemNeutral(songs)

songsForDeletion = list(set(songs) - set(curSongList))

print(songs)
print("Cur: \n")
print(curSongList)
print("Deletion: \n")
print(songsForDeletion)

for item in songsForDeletion:
    try:
        os.remove(config['destination'] + "/" + item)
        print("Removed " + item)
    except FileNotFoundError:
        print("Could not remove " + item)

## If -t flag add ID3 tags to files
if tagFiles: 
    proc = sp.Popen(['python', 'mp3tags.py', '-p', config['destination']], stdout=sp.PIPE, stderr=sp.PIPE)
    result = proc.communicate()[1]

    result = str(result).replace('\\n', '\n').replace("\\\'", '\'')

    if not proc.returncode:
        print("ID3 Tagged Files")
    else:
        print("\nFailed to tag files\n" + result)
