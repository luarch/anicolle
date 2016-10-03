#!/usr/bin/env python3
import requests
import re as _re
import xml.etree.ElementTree as ET

def seek(chk_key, cur_epi):
    # Compose search keyword
    tepi = cur_epi+1
    chk_key = str(chk_key)
    chk_key = "%s %02d" % (chk_key, tepi)

    # Get search result page
    url = "https://share.dmhy.org/topics/rss/rss.xml?keyword={}".format(chk_key)
    r = requests.get(url, timeout=2)
    r.encoding = "utf-8"

    tree = ET.fromstring(r.text)

    r = []
    for item in tree.iterfind("channel/item"):
        r.append({"title": item.find("title").text, "link": item.find('enclosure').get('url')})

    if len(r) == 0:
        return 0
    else:
        return r

if __name__ == '__main__':
    r = seek("【极影字幕社】 重装武器", 9)
    if r:
        for i in r:
            print(i['title'])
            print(i['link'])
    else:
        print('Not found')
