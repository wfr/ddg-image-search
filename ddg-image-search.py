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
import urllib
import os
import shutil
import argparse
import tempfile

import ddg

# We use PIL because imghdr does not reliably recognize some JPEG images.
from PIL import Image


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
parser.add_argument('--limit', type=int, default=50)
parser.add_argument('--destdir', type=str, required=True)
# parser.add_argument('--layout', choices=['all', 'aspect-square'], default="all")
args = parser.parse_args()

if not os.path.exists(args.destdir):
    os.makedirs(args.destdir)

ddi = ddg.DuckDuckImages()
i = 0
for obj in ddi.search(args.term, size=args.size, type=args.type, safe_search=args.safe_search, limit=args.limit):
    domain = urllib.parse.urlparse(obj["image"]).netloc
    fn = "%06d-" % i + urllib.parse.quote_plus(obj["image"])
    fp = os.path.join(args.destdir, fn)
    download_image(obj["image"], fp)
    i += 1

# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
