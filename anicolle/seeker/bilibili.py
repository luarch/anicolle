import requests
from bs4 import BeautifulSoup
from json import loads

def seek(chk_key, cur_epi):
    tepi = cur_epi+1
    chk_key = str(chk_key)

    try:
        int(chk_key)
    except ValueError:
        query_url = "http://www.bilibili.com/search?keyword=%s&orderby=&type=series&tids=&tidsC=&arctype=all&page=1" % (chk_key, )
        html_content = requests.get(query_url).text
        bs = BeautifulSoup(html_content, "html.parser")
        s_bgmlist = bs.find('div', class_="s_bgmlist")
        try:
            season_id = s_bgmlist.get('data-seasonid')
        except AttributeError:
            return {}
    else:
        season_id = chk_key

    api_url = "http://app.bilibili.com/bangumi/seasoninfo/%s.ver?callback=episodeJsonCallback" % (season_id,)
    apiRes = requests.get(api_url).text
    apiRes = apiRes[20:]
    apiRes = apiRes[:-1]
    apiRes = loads(apiRes)
    epi_list = apiRes['result']['episodes']

    try:
        for epi in  epi_list:
            if epi['index'] == str(tepi):
                av_id = epi['av_id']
                av_page= epi['page']
                av_name = epi['index_title']
                break
        else:
            raise IndexError;
    except IndexError:
        return 0

    link = "http://www.bilibili.com/video/av%s/index_%s.html" % (av_id, av_page)
    title = "%s - %d from Bilibili" % (av_name, tepi)

    return {'link': link, 'title': title}

