import bs4

COMMENT_MAX=100
USER_FILM_MAX=100
SLEEP_TIME=0.5
headers={
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8'
        ,'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5'
        ,'Cache-Control': 'max-age=0'
        ,'Connection': 'Keep-Alive'
        ,'Cookie': '__utmc=223695111; __utmz=223695111.1602399324.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1602411375%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=fe4c05d746b29034.1602395250.3.1602412991.1602401814.; __utma=223695111.997758845.1602395250.1602399324.1602411375.3; _pk_ses.100001.4cf6=*; __utmb=223695111.0.10.1602411375; __yadk_uid=qfmxz2maPjrnFUpBu2INhHHvzelYSQl5; __utmc=30149280; __utmz=30149280.1602399324.4.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ll="108288"; _vwo_uuid_v2=D3E3229A4D790E83637E63D358C7399F8|007c2dd0330c657228433d0c294a33ae; __gads=ID=50a3fe7d3fd21b76:T=1602395254:S=ALNI_MYeijA_iOl2HXUHdG6lPo_WtDhsJg; ap_v=0,6.0; bid=_h2ZhUpcR58; __utma=30149280.584000826.1592147609.1602399324.1602411375.5; __utmb=30149280.2.10.1602411375; douban-fav-remind=1'
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