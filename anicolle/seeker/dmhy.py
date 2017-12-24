#!/usr/bin/env python3
import requests
import re as _re
import xml.etree.ElementTree as ET


def seek(chk_key, cur_epi, params):
    """DMHY Seeker

    Seeks from: http://share.dmhy.org

    Support params:
    tepi_pad_size -- the padding size of episode number for seeking (default 2)
    """
    tepi_pad_size = 2
    if params and len(params) >= 1:
        tepi_pad_size = int(params[0])

    # Compose search keyword
    tepi = cur_epi+1
    tepi = str(tepi).zfill(tepi_pad_size)
    chk_key = str(chk_key)
    chk_key = "%s %s" % (chk_key, tepi)

    # Get search result page
    url = ("https://share.dmhy.org/topics/rss/rss.xml"
           "?keyword={}").format(chk_key)

    r = requests.get(url, timeout=2)
    r.encoding = "utf-8"

    tree = ET.fromstring(r.text)

    r = []
    for item in tree.iterfind("channel/item"):
        # TODO Filter through results
        if isValid(item, tepi):
            r.append({
                "title": item.find("title").text,
                "link": item.find('enclosure').get('url')
                })

    if len(r) == 0:
        return 0
    else:
        return r


def isValid(item, tepi):
    title = item.find("title").text
    pattern = "( |\[|{|第|【|〖)"
    pattern += _re.escape(tepi)
    pattern += "(\]|话|話|集|〗|】|END| )"
    match = _re.search(pattern, title)
    return match


if __name__ == '__main__':
    r = seek("vrains", 9, ("3"))
    if r:
        for i in r:
            print(i['title'])
            print(i['link'])
    else:
        print('Not found')
