#!/usr/bin/env python

import json
from pprint import pprint
import urllib.request as REQ
import subprocess as sp
import os
from os.path import isfile, join
import sys
import argparse

def loadConfigFile():
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + "/config.json", "r") as configFile:
            data = configFile.read()
            jsonObj = json.loads(data)
            return jsonObj
    except FileNotFoundError:
        return False

def writeDefaultConfig():
    xdgConfig = os.getenv('XDG_CONFIG_HOME')
    configList = {'playlistID': 'PLP37tSKMt8KzgfdABgSZQ2wV2IirbTOPR', 'googleAPIKey': 'PUT KEY HERE', 'destination': '/home/shane/Music'}

    jsonSaveFile = json.dumps(configList, indent=4)
    with open(os.path.dirname(os.path.realpath(__file__)) + "/config.json", "w") as configFile:
        print(jsonSaveFile, file=configFile)


def deleteList(songList):
    dirFiles = [f for f in os.listdir("./") if isfile(join("./", f))]

    for item in dirFiles:
        for song in songList:
            if song in item:
                os.remove(item)
                print("Removed " + song)
                dirFiles.remove(item)
                songList.remove(song)

    return True
    

def loadSongList(path):
    try:
        with open(path + "/songlist.json", "r") as jsonFile:
            data = jsonFile.read()
            jsonObj = json.loads(data)
            return jsonObj
    except FileNotFoundError:
        return False

def saveSongList(songList, path):
    jsonSaveFile = json.dumps(songList)
    with open(path + "/songlist.json", "w") as jsonFile:
        print(jsonSaveFile, file=jsonFile)

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

# BEGIN EXECUTION

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--id3tag', help="Automatically sets up ID3 tags based on '-' delimiter. Requires optional dependency 'python-mutagen'", action="store_true")
parser.add_argument('-v', '--verbose', help="Includes skipped songs(Already downloaded and in active playlist)", action="store_true")
args = parser.parse_args()

tagFiles = False
verbose = False

if args.id3tag:
   tagFiles = True

if args.verbose:
    verbose = True

config = loadConfigFile()

if not config:
    writeDefaultConfig()
    print("No config, wrote default. Ensure to edit appropriately")
    sys.exit(1)

url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=" + config['playlistID'] + "&key=" + config['googleAPIKey'] + "&maxResults=50"


page = downloadPage(url)
jsonData = decodeJson(page)

songs = loadSongList(config['destination'])

if songs is False:
    songs = []

curSongList = []

for items in jsonData['items']:
    curSongList.append(items['snippet']['title'])
    if items['snippet']['title'] not in songs:
        print("Downloading " + items['snippet']['title'] + "..")
        if downloadVideo("https://youtube.com/watch?v=" + items['snippet']['resourceId']['videoId'], config['destination']):
            songs.append(items['snippet']['title'])
        else:
            print("\n--DOWNLOAD FAILED--\n")
    else:
        if verbose:
            print("SKIPPING " + items['snippet']['title'])

songsForDeletion = list(set(songs) - set(curSongList))

songs = list(set(songs) - set(songsForDeletion))

# Add Tags
if tagFiles: 
    proc = sp.Popen(['python', 'mp3tags.py', '-p', config['destination']], stdout=sp.PIPE, stderr=sp.PIPE)
    result = proc.communicate()[1]

    result = str(result).replace('\\n', '\n').replace("\\\'", '\'')

    if not proc.returncode:
        print("ID3 Tagged Files")
    else:
        print("\nFailed to tag files\n" + result)


deleteList(songsForDeletion)
saveSongList(songs, config['destination'])
