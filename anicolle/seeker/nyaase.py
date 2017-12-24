#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
import urllib.parse


def seek(chk_key, cur_epi, params):
    # Compose search keyword
    tepi = cur_epi+1
    tepi = str(tepi).zfill(2)
    chk_key = str(chk_key)
    chk_key = "%s %s" % (chk_key, tepi)
    chk_key = urllib.parse.quote_plus(chk_key)

    # Get search result page
    url = "http://nyaa.pantsu.cat/feed?c=_&s=0&limit=50\
&userID=0&q={}".format(chk_key)
    r = requests.get(url, timeout=5)
    r.encoding = "utf-8"

    print(r.text)
    tree = ET.fromstring(r.text)

    r = []
    for item in tree.iterfind("channel/item"):
        r.append({"title": item.find("title").text,
                  "link": item.find('guid').text})

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
