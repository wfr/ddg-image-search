#!/usr/bin/env python3
"""
ddg-image-search - search for images on DuckDuckGo and download them.

Copyright (C) 2019 Wolfgang Frisch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import requests
import re
import sys
import urllib
import os
import shutil
import argparse
import tempfile

# We use PIL because imghdr does not reliably recognize some JPEG images.
from PIL import Image


class DuckDuckImages():
    def __init__(self):
        self.s = requests.Session()

    def search(self, term, size="all", safe_search="off", type="all", limit=50):
        """
        size: all, small, medium, large, wallpaper
        safe_search: off, moderate, strict
        type: all, photo, clipart, gif, transparent

        Returns generator of:
        {
        'image': 'https://....',
        'source': 'Yahoo',
        'thumbnail': 'https://....',
        'title': 'Foobar',
        'url': 'https://....',
        'width': 123,
        'height': 456,
        }
        """
        iaf = []
        if size != "all":
            iaf.append("size:" + size)
        if type != "all":
            iaf.append("type:" + type)
        # print(",".join(iaf))

        if safe_search == "off":
            self.s.cookies["p"] = "-2"
        elif safe_search == "moderate":
            self.s.cookies["p"] = "-1"

        # Acquire vqd token
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://duckduckgo.com/",
            "DNT": "1",
        }
        params = {
            "q": term,
            "t": "ffsb",
            # "ia": "images",
            # "iax": "images",
            "iar": "images",
            "iaf": ",".join(iaf),
        }
        req = self.s.get("https://duckduckgo.com", params=params, headers=headers)
        sr = re.search(r'vqd=([\d-]+)\&', req.text, re.M | re.I)
        if not sr:
            print("vqd token not found. Status code: %d" % req.status_code)
            sys.exit(1)
        vqd = sr.group(1)
        # print("vqd token: " + vqd)
        print(req.request.url)

        # Actual search
        self.s.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Referer": "https://duckduckgo.com/",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
        }
        params = {
            "f": ",".join(iaf),
            "l": 'wt-wt',
            "o": "json",
            "p": -1,  # ???
            "q": term,
            "s": 0,
            "iaf": ",".join(iaf),
            # "u": "yahoo", # ???
            "vqd": vqd,
        }

        # necessary?
        if safe_search == "off":
            params["ex"] = -2
        elif safe_search == "moderate":
            params["ex"] = -1

        n = 0
        while n < limit:
            params["s"] = n
            req = self.s.get("https://duckduckgo.com/i.js", params=params)
            if (req.status_code != 200):
                print("HTTP status %d" % req.status_code)
                sys.exit(1)
            # print(req.text)
            if len(req.json()["results"]):
                for obj in req.json()["results"]:
                    yield obj
            else:
                return
            n += 50


def download_image(url, path, add_extension=True):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
    }
    try:
        print("Downloading ... " + url)
        with tempfile.NamedTemporaryFile() as temp:
            req = requests.get(url, stream=True, headers=headers)
            if req.status_code != 200:
                print("    HTTP status: %d" % req.status_code)
            shutil.copyfileobj(req.raw, temp)
            del req
            ext = Image.open(temp.name).format.lower()
            print("    image type: %s" % ext)
            if ext:
                shutil.copyfile(temp.name, path + "-." + ext)
                return True
    except requests.exceptions.ConnectionError:
        print("    ConnectionRefusedError " + url)
    except OSError:
        print("    cannot identify image format")
    return False


parser = argparse.ArgumentParser(description='Search for images on DuckDuckGo.')
parser.add_argument('term', type=str, help='search term')
parser.add_argument('--safe-search', choices=['off', 'moderate', 'strict'], default="off")
parser.add_argument('--type', choices=['all', 'photo', 'clipart', 'gif', 'transparent'], default="all")
parser.add_argument('--size', choices=['all', 'small', 'medium', 'large', 'wallpaper'], default="all")
parser.add_argument('--limit', type=int, default=50, help="download at most N images (default 50)")
parser.add_argument('-d', '--destdir', type=str, required=True)
# parser.add_argument('--layout', choices=['all', 'aspect-square'], default="all")
args = parser.parse_args()

if not os.path.exists(args.destdir):
    os.makedirs(args.destdir)

ddi = DuckDuckImages()
i = 0
for obj in ddi.search(args.term, size=args.size, type=args.type, safe_search=args.safe_search, limit=args.limit):
    domain = urllib.parse.urlparse(obj["image"]).netloc
    fn = "%06d-" % i + urllib.parse.quote_plus(obj["image"])
    fp = os.path.join(args.destdir, fn)
    download_image(obj["image"], fp)
    i += 1

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
