'''
获取电影信息
'''
import requests
import util
from bs4 import BeautifulSoup
import actor
import re
import sql
import time
import proxy
import log
class film:
    film_id=""
    film_name=""
    director=""
    screenwriter=""
    mainactors=""
    film_type=""
    area=""
    lang=""
    film_date=""
    film_time=""
    film_alias=""
    imdb=""
    score=""
    film_summary=""
    
    def get_film(self,film_id):
        r=proxy.gethtml(url='https://movie.douban.com/subject/'+str(film_id),headers=util.headers,params={})
        if r is None:
            return
        soup=BeautifulSoup(r.content.decode(),'html.parser')
        if r is None:
            return
        
        self.film_id=str(film_id)
        lst=soup.find_all('span',attrs={'property':'v:itemreviewed'})
        if lst:
            self.film_name=util.listtostr(lst,'')

        lst=soup.find_all('a',attrs={'rel':'v:directedBy'})
        if lst:
            self.director=util.listtostr(lst,"/")
        
        sw=soup.find('span',attrs={'class':'pl'},text='编剧')
        if sw:
            swn=sw.find_next_sibling('span')
            if swn:
                swna=swn.find_all('a')
                if swna:
                    self.screenwriter=util.listtostr(swna,'/')

        lst=soup.find_all('a',attrs={'rel':'v:starring'})
        if lst:
            self.mainactors=util.listtostr(lst,"/")
        
        lst=soup.find_all('span',attrs={'property':'v:genre'})
        if lst:
            self.film_type=util.listtostr(lst,'/')

        
        sw=soup.find('span',attrs={'class':'pl'},text='制片国家/地区:')
        if sw:
            swn=sw.next_sibling
            if swn:
                self.area=swn.strip()
        

        sw=soup.find('span',attrs={'class':'pl'},text='语言:')
        if sw:
            swn=sw.next_sibling
            if swn:
                self.lang=swn.strip()
        
        lst=soup.find_all('span',attrs={'property':'v:initialReleaseDate'})
        if lst:
            self.film_date=util.listtostr(lst,'/')

        lst=soup.find_all('span',attrs={'property':'v:runtime'})
        if lst:
            self.film_time=util.listtostr(lst,'/')


        
        sw=soup.find('span',attrs={'class':'pl'},text='又名:')
        if sw:
            swn=sw.next_sibling
            if swn:
                self.film_alias=swn.strip()

        
        sw=soup.find('span',attrs={'class':'pl'},text='IMDb链接:')
        if sw:
            swn=sw.next_sibling
            if swn:
                self.imdb=swn.strip()


        sf=soup.find('strong',attrs={'property':'v:average'})
        if sf:
            self.score=sf.get_text()

        sf=soup.find('span',attrs={'property':'v:summary'})
        if sf:
            self.film_summary=sf.get_text().strip()

    def get_actor_info(self,act):
        r=proxy.gethtml(url='https://movie.douban.com/celebrity/'+str(act.actor_id),headers=util.headers,params={})
        if r is None:
            return 
        soup=BeautifulSoup(r.content.decode(),'html.parser')
        if soup is None:
            return

        gt=soup.find('span',text='性别')
        if gt:
            sf=gt.next_sibling
            if sf:
                act.gender=sf.replace(':','').strip()
        
        gt=soup.find('span',text='星座')
        if gt:
            sf=gt.next_sibling
            if sf:
                act.xingzuo=sf.replace(':','').strip()
        
        gt=soup.find('span',text='出生日期')
        if gt:
            sf=gt.next_sibling
            if sf:
                act.birthday=sf.replace(':','').strip()

        gt=soup.find('span',text='出生地')
        if gt:
            sf=gt.next_sibling
            if sf:
                act.birtharea=sf.replace(':','').strip()
        
        gt=soup.find('span',text='职业')
        if gt:
            sf=gt.next_sibling
            if sf:
                act.occupation=sf.replace(':','').strip()

        gt=soup.find('span',text='更多中文名')
        if gt:
            sf=gt.next_sibling
            if sf:
                act.more_name=sf.replace(':','').strip()
        
        gt=soup.find('span',text='更多外文名')
        if gt:
            sf=gt.next_sibling
            if sf:
                act.more_foreign_name=sf.replace(':','').strip()
        
        gt=soup.find('span',text='imdb编号')
        if gt:
            gta=gt.find_next_sibling('a')
            if gta:
                act.imdb_id=gta.get_text()
        
        gt=soup.find('span',text='官方网站')
        if gt:
            gta=gt.find_next_sibling('a')
            if gta:
                act.web_url=gta.get_text()


    def get_actors(self,film_id):
        r=proxy.gethtml(url='https://movie.douban.com/subject/'+str(film_id)+'/celebrities',headers=util.headers,params={})
        if r is None:
            return
        soup=BeautifulSoup(r.content.decode(),'html.parser')
        if soup is None:
            return
        
        lis=soup.find_all('li',{'class':'celebrity'})
        if lis is None:
            return
        for li in lis:
            act=actor.actor()
            sf=li.find('span',{'class':'name'})
            if sf:
                sfa=sf.find('a')
                if sfa:
                    act.actor_name=sfa.get_text()
                    ar=re.search(r'(\d+)\/?$',sfa.get('href'))
                    if ar:
                        act.actor_id=ar.group(1)
            if act.actor_id=="":
                continue
            
            sf=li.find('span',{'class':'role'})
            if sf:
                act.actor_role=sf.get_text()
            
            sf=li.find('span',{'class':'works'})
            if sf:
                sfa=sf.find_all('a')
                if sfa:
                    act.main_works=util.listtostr(sfa,'/')


            dbacts=sql.get_actor_byid(act.actor_id)
            try:
                if len(dbacts)==0:
                    self.get_actor_info(act)
                    sql.save_actor(act)
                dbactfs=sql.get_actor_film_byid(act.actor_id,film_id)
                if len(dbactfs)==0:
                    sql.save_actor_film(act.actor_id,film_id,act.actor_role)
            except Exception as e:
                log.logger.info(str(e))
            print(act)
                      

    def save(self):
        try:
            flms=sql.get_film_byid(self.film_id)
            if len(flms)==0:
                sql.insert_film(self)
            else:
                sql.update_film_byid(self)
        except Exception as e:
            log.logger.info(str(e))
'''
f=film()
f.get_film(25907124)
f.save()
'''
