#!/usr/bin/env python

from bs4 import BeautifulSoup

import requests
import track
import sys
import re

if __name__ == "__main__":
    track_no_regex = r"^(\d+)(?:\.) "

    print("####    Rockit Downloader   ####")
    print("####  Powered by @debba_92  ####")
    print("####  Modified by @lbrdan  ####")

    if len(sys.argv) < 2:
        print("Usage: ./download.py <album_url>\n")
        exit(0)

    rockitUrl = sys.argv[1]

    rockitPage = requests.get(rockitUrl).text
    soup = BeautifulSoup(rockitPage, 'html.parser')
    soup.prettify()

    infodiv = soup.find('div', {"class": "info"})
    author = infodiv.h2.text.strip()
    album = infodiv.h1.text.strip()
    referer = rockitUrl

    print("[INFO] Download album: " + album +
          ", author: " + author + " started.\n")

    album_id = soup.find('div', {"class": "playerContainer"})['data-id']

    tracklist_ul = soup.find('ul', {"class": "tracklist"})

    for item in tracklist_ul.contents:

        if item is None or item['data-rel'] is None:
            continue

        m = re.match(track_no_regex, item.span.text.strip())

        track_no = -1
        if len(m.groups()) == 1:
            track_no = m.groups()[0]

        rt = track.RockitTrack(
            item['data-rel'], album_id, album, track_no, referer)
        rt.download(requests)
