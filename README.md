# Youtube-Music-Sync
Command-line utility for maintaining an active repository of music in YouTube playlist

[![Build Status](https://travis-ci.org/SajeOne/Youtube-Music-Sync.svg?branch=dev "Dev")](https://travis-ci.org/SajeOne/Youtube-Music-Sync)
[![Build Status](https://travis-ci.org/SajeOne/Youtube-Music-Sync.svg?branch=master "Master")](https://travis-ci.org/SajeOne/Youtube-Music-Sync)
[![Code Climate](https://codeclimate.com/github/SajeOne/Youtube-Music-Sync/badges/gpa.svg)](https://codeclimate.com/github/SajeOne/Youtube-Music-Sync)

![Youtube-Sync Image](https://i.imgur.com/W6g9E5H.png "Example use of Youtube-Sync")


### Optional Dependencies:
```
python-mutagen
```

## Installation
```
$ git clone https://github.com/SajeOne/Youtube-Music-Sync.git
Cloning into 'Youtube-Music-Sync'...
remote: Counting objects: 67, done.
remote: Compressing objects: 100% (61/61), done.
remote: Total 67 (delta 36), reused 22 (delta 5), pack-reused 0
Unpacking objects: 100% (67/67), done.
Checking connectivity... done.

$ cd Youtube-Music-Sync/

$ sudo ./install.sh
Youtube-Music-Sync Installed, type "youtube-sync" to execute it

$ youtube-sync -h
usage: youtube-sync [-h] [-t] [-v] [-s]

optional arguments:
  -h, --help      show this help message and exit
  -t, --id3tag    Automatically sets up ID3 tags based on '-' delimiter.
                  Requires optional dependency 'python-mutagen'
  -v, --verbose   Includes skipped songs(Already downloaded and in active
                  playlist)
  -s, --simulate  Simulates without actually downloading, good for speed
                  testing
```
