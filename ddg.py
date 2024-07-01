#!/usr/bin/env python3
import re
import requests
import sys


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


# vim:set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
