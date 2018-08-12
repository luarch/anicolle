#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from json import loads
import re
from ..config import config


def seek(chk_key, epi, params):
    tepi = epi
    chk_key = str(chk_key)

    try:
        int(chk_key)
    except ValueError:
        query_url = ("http://search.bilibili.com/bangumi"
                     "?keyword=%s") % (chk_key, )
        html_content = requests.get(query_url, timeout=2, proxies=config['seekerProxies']).text
        bs = BeautifulSoup(html_content, "html.parser")
        s_bgmlist = bs.find('div', class_="ajax-render")
        try:
            season_id = s_bgmlist.find('a', class_="title").get('href')
            season_id = re.findall('\d+', season_id)
            if len(season_id):
                season_id = season_id[0]
            else:
                raise AttributeError
        except AttributeError:
            return 0
    else:
        season_id = chk_key

    api_url = ("http://app.bilibili.com/bangumi/seasoninfo/%s.ver"
               "?callback=seasonListCallback") % (season_id,)
    apiRes = requests.get(api_url, timeout=2).text
    apiRes = re.sub("^.+?\(", '', apiRes)
    apiRes = re.sub("\);", '', apiRes)
    apiRes = loads(apiRes)
    epi_list = apiRes['result']['episodes']

    av_name = apiRes['result']['title']

    try:
        for epi in epi_list:
            if epi['index'] == str(tepi):
                av_id = epi['av_id']
                av_page = epi['page']
                break
        else:
            raise IndexError
    except IndexError:
        return 0

    link = ("http://www.bilibili.com/video/"
            "av%s/index_%s.html") % (av_id, av_page)
    title = "%s - %d from Bilibili" % (av_name, tepi)

    return [{'link': link, 'title': title}]


if __name__ == '__main__':
    test_r = seek("食戟之灵 贰之皿", 10, ())
    print(test_r)
