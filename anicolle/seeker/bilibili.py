#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from json import loads
import re

def seek(chk_key, cur_epi):
    tepi = cur_epi+1
    chk_key = str(chk_key)

    try:
        int(chk_key)
    except ValueError:
        query_url = "http://search.bilibili.com/bangumi?keyword=%s" % (chk_key, )
        html_content = requests.get(query_url).text
        bs = BeautifulSoup(html_content, "html.parser")
        s_bgmlist = bs.find('div', class_="ajax-render")
        try:
            season_id = s_bgmlist.find('a').get('href')
            season_id = re.findall('\d+', season_id)
            if len(season_id):
                season_id = season_id[0]
            else:
                raise AttributeError
        except AttributeError:
            return 0
    else:
        season_id = chk_key

    api_url = "http://app.bilibili.com/bangumi/seasoninfo/%s.ver?callback=episodeJsonCallback" % (season_id,)
    apiRes = requests.get(api_url).text
    apiRes = apiRes[20:]
    apiRes = apiRes[:-2]
    apiRes = loads(apiRes)
    epi_list = apiRes['result']['episodes']

    av_name = apiRes['result']['title']

    try:
        for epi in  epi_list:
            if epi['index'] == str(tepi):
                av_id = epi['av_id']
                av_page= epi['page']
                break
        else:
            raise IndexError;
    except IndexError:
        return 0

    link = "http://www.bilibili.com/video/av%s/index_%s.html" % (av_id, av_page)
    title = "%s - %d from Bilibili" % (av_name, tepi)

    return {'link': link, 'title': title}

if __name__ == '__main__':
    seek("粗点心战争", 0)
