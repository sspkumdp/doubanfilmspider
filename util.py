import bs4

COMMENT_MAX=100
USER_FILM_MAX=100
SLEEP_TIME=1
headers={
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8'
        ,'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5'
        ,'Cache-Control': 'max-age=0'
        ,'Connection': 'Keep-Alive'
        ,'Host': 'movie.douban.com'
        ,'Upgrade-Insecure-Requests': '1'
        ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
        }

def listtostr(list,sep):
    re=""
    for i in list:
        if re!="":
            re+=sep
        re+=i.get_text()
    return re


def content_to_str(cont,sep):
    re=""
    for c in cont:
        
        s=''
        if type(c) is bs4.element.NavigableString:
            s=c.strip()
        elif type(c) is bs4.element.Tag:
            s=c.get_text().strip()
        if len(s)>0:
            if re!="":
                re+=sep
            re+=s
        
    return re
