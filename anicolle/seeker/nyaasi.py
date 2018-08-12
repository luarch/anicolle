#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
import urllib.parse
from ..config import config


def seek(chk_key, epi, params):
    # Compose search keyword
    tepi = epi
    tepi = str(tepi).zfill(2)
    chk_key = str(chk_key)
    chk_key = "%s %s" % (chk_key, tepi)
    chk_key = urllib.parse.quote_plus(chk_key)

    # Get search result page
    url = "https://nyaa.si/?page=rss&q={}&c=0_0&f=0".format(chk_key)
    r = requests.get(url, timeout=10, proxies=config['seekerProxies'])
    r.encoding = "utf-8"

    print(r.text)
    tree = ET.fromstring(r.text)

    r = []
    for item in tree.iterfind("channel/item"):
        r.append({"title": item.find("title").text,
                  "link": item.find('link').text})

    if len(r) == 0:
        return 0
    else:
        return r


if __name__ == '__main__':
    r = seek("All Out!! Ohys", 14, ())
    if r:
        for i in r:
            print(i['title'])
            print(i['link'])
    else:
        print('Not found')
