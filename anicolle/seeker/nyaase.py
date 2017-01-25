#!/usr/bin/env python3
import requests
import re as _re
import xml.etree.ElementTree as ET
import urllib.parse

def seek(chk_key, cur_epi):
    # Compose search keyword
    tepi = cur_epi+1
    chk_key = str(chk_key)
    chk_key = "%s %02d" % (chk_key, tepi)
    chk_key = urllib.parse.quote_plus(chk_key)

    # Get search result page
    url = "https://www.nyaa.se/?page=rss&term={}".format(chk_key)
    r = requests.get(url, timeout=2)
    r.encoding = "utf-8"

    tree = ET.fromstring(r.text)

    r = []
    for item in tree.iterfind("channel/item"):
        r.append({"title": item.find("title").text, "link": item.find('link').text})

    if len(r) == 0:
        return 0
    else:
        return r

if __name__ == '__main__':
    r = seek("All Out!! Ohys", 14)
    if r:
        for i in r:
            print(i['title'])
            print(i['link'])
    else:
        print('Not found')
