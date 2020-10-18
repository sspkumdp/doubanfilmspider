import util
import requests
import re
from bs4 import BeautifulSoup
import film
import time
import sql
import proxy
import log
class user:
    user_id=""
    user_name=""
    user_url=""
    viewed_count=""
    wish_count=""
    user_area=""
    user_time=""
    user_info=""
    visible=""
    headers={
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8'
        ,'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5'
        ,'Cache-Control': 'no-cache'
        ,'Connection': 'Keep-Alive'
        ,'Host': 'www.douban.com'
        ,'Upgrade-Insecure-Requests': '1'
        ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
    }
    def get_viewed_films(self,user_url):
        r=proxy.gethtml(url=user_url+'/collect?start=0',headers=self.headers,params={})
        if r is None:
            return
        soup=BeautifulSoup(r.content.decode(),'html.parser')
        if soup is None:
            return

        movien=soup.find('div',{'class':'info'})
        tot=0
        if movien:
            sf=movien.find('h1')
            if sf:
                a=sf.get_text()
                ar=re.search(r'\((.+)\)',a)
                self.viewed_count=ar.group(1)
                tot=int(self.viewed_count)
        
        if tot>util.USER_FILM_MAX:
            tot=util.USER_FILM_MAX

        for i in range(0,int(tot/15)+1):
            r=proxy.gethtml(url=user_url+'/collect?start='+str(i*15),headers=util.headers,params={})
            if r is None:
                continue
            soup=BeautifulSoup(r.content.decode(),'html.parser')
            if soup is None:
                continue
            items=soup.find_all('div',{'class':'item'})
            if items is None:
                continue
            for item in items:
                a=item.find('a')
                if a is None:
                    continue
                film_id_ref=a.get('href')
                refr=re.search(r'(\d+)\/?$',film_id_ref)
                if refr:
                    film_id=refr.group(1)
                    try:
                        flms=sql.get_film_byid(film_id)
                        if len(flms)==0:
                            f=film.film()
                            f.film_id=film_id
                            f.save()
                    except Exception as e:
                        log.logger.info(str(e))

    def get_user_info(self,user_url):
        r=proxy.gethtml(url=user_url,headers=self.headers,params={})
        if r is None:
            self.visible='0'
            return
        soup=BeautifulSoup(r.content.decode(),'html.parser')
        if soup is None:
            self.visible='0'
            return
        ui=soup.find('div',{'class':'user-info'})
        if ui:
            self.visible='1'
            uia=ui.find('a')
            if uia:
                self.user_area=uia.get_text()
            uid=ui.find('div',{'class':'pl'})
            if uid:
                uids=util.content_to_str(uid,' ')
                uidsr=re.search(r'(\d\d\d\d-\d\d-\d\d)',uids)
                if uidsr:
                    self.user_time=uidsr.group(1)
            uii=soup.find('span',id='intro_display')
            if uii:
                self.user_info=util.content_to_str(uii,' ')
        else:
            self.visible='0'
        
        mv=soup.find('div',id='movie')
        if mv:
            mvs=mv.find('span',{'class':'pl'})
            if mvs:
                mvsas=mvs.find_all('a')
                for mvsa in mvsas:
                    if "部想看" in mvsa.get_text():
                        self.wish_count=mvsa.get_text().replace('部想看','')
                    elif "部看过" in mvsa.get_text():
                        self.viewed_count=mvsa.get_text().replace('部看过','')
        


'''
user=user()
user.get_user_info('https://www.douban.com/people/darkwood')
'''
