import urllib.request as _ur
import urllib.parse as _up
import re as _re

def seek(chk_key, cur_epi):
    tepi = cur_epi+1
    chkkey = str(chk_key) + " " + "%02d"%tepi
    chkkey = _up.quote_plus(chkkey)

    r = _ur.urlopen( "http://share.popgo.org/search.php?title=%s&sorts=1"%chkkey ).read().decode('utf-8')
    re1 = _re.compile( '查看详情页.*?title="([^"]*' + '%02d'%tepi + '[集话\]】\[][^"]*)".*?(magnet[^"]*)"' )
    maglink = _re.search(re1, r)
    if maglink:
        magname = maglink.group(1)
        maglink = maglink.group(2)
        return { "magname": magname, "maglink": maglink }
    else:
        return 0

