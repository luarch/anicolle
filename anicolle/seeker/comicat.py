#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re as _re

def seek(chk_key, cur_epi):
    # Compose search keyword
    tepi = cur_epi+1
    chk_key = str(chk_key)
    chk_key = "%s %02d" % (chk_key, tepi)

    # Get search result page
    url = "http://www.comicat.org/search.php?keyword=%s"%(chk_key, )
    r = requests.get(url).text

    # Find resource page
    title = ""
    resource_url = ""
    bs = BeautifulSoup(r, "html.parser")
    table = bs.find(id='listTable')
    rows_with_link = table.find_all('tr')
    for row_with_link in rows_with_link:
        title = ''
        cells_with_link = row_with_link.find_all('td')
        if not cells_with_link or len(cells_with_link)<3:
            continue
        cell_with_link = cells_with_link[2]
        anchor_with_link = cell_with_link.find('a')
        if anchor_with_link:
            for string in anchor_with_link.strings:
                title += string
            title = title.strip()
            if( '%02d月'%tepi in title and not _re.search('%02d'%tepi + '.*' + '%02d'%tepi, title)):
                continue
            else:
                resource_url = "http://www.comicat.org/" + anchor_with_link.get('href')
                break

    # Open resource page and find maglink
    if resource_url:
        r = requests.get(resource_url).text
        bs = BeautifulSoup(r, 'html.parser')
        anchor_with_maglink = bs.find(id='magnet')
        link = anchor_with_maglink.get('href')
        return { "title": title, "link": link }
    else:
        return 0

if __name__ == '__main__':
    r = seek("【极影字幕社】 重装武器", 9)
    if r:
        print(r['title'])
        print(r['link'])
    else:
        print('Not found')
