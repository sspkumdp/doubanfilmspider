import sql
import film
import comments_by_film
import user
import time
import proxy
import util
from bs4 import BeautifulSoup
import re
from urllib import parse
class pipeline:
    headers={
            'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8'
            ,'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5'
            ,'Connection': 'Keep-Alive'
            ,'Cookie': '__utmz=223695111.1602590741.13.7.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1602598782%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=fe4c05d746b29034.1602395250.14.1602599165.1602593338.; __utma=223695111.997758845.1602395250.1602590741.1602598782.14; _pk_ses.100001.4cf6=*; __utmb=223695111.0.10.1602598782; __yadk_uid=qfmxz2maPjrnFUpBu2INhHHvzelYSQl5; __utmc=223695111; __utmz=30149280.1602483789.9.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/darkwood/; ll="108288"; _vwo_uuid_v2=D3E3229A4D790E83637E63D358C7399F8|007c2dd0330c657228433d0c294a33ae; __gads=ID=50a3fe7d3fd21b76:T=1602395254:S=ALNI_MYeijA_iOl2HXUHdG6lPo_WtDhsJg; ap_v=0,6.0; bid=_h2ZhUpcR58; __utma=30149280.584000826.1592147609.1602590736.1602598782.17; __utmb=30149280.0.10.1602598782; douban-fav-remind=1; ct=y; __utmc=30149280'
            ,'Host': 'movie.douban.com'
            ,'Referer': 'https://movie.douban.com/explore'
            ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
            ,'X-Requested-With': 'XMLHttpRequest'
        }
    def run1film(self,film_id):
        dbflms=sql.get_film_byid(film_id)
        if len(dbflms)>0:
            if dbflms[0]['spider']=='1':
                return
        f=film.film()
        #获取电影信息
        f.get_film(film_id)
        #获取演职员信息
        f.get_actors(film_id)
        #保存数据库
        f.save()

        #获取评论和用户信息并保存
        cf=comments_by_film.comments()
        cf.get_comments_by_film(film_id)
        
        #修改数据库电影状态为已爬
        sql.update_film_spider(film_id)

    def run(self,film_id):
        self.run1film(film_id)
        self.run_unspider()
        

    def run_unspider(self):

        #获取数据库中已存但还没爬的电影
        unsflms=sql.get_unspider_film()
        for flm in unsflms:
            self.run1film(flm['film_id'])
        
        #获取数据库中已存，但还没爬他看过的电影的用户
        unsusers=sql.get_unspider_user()
        for dbu in unsusers:
            u=user.user()
            u.user_id=dbu['user_id']
            #获取该用户看过的电影并存入数据库
            u.get_viewed_films(dbu['user_url'])
            #修改用户状态为已爬过
            sql.update_user_spider(u.user_id)
        
        time.sleep(3)
        self.run_unspider()

    def run_hot(self):
        for i in range(0,11):
            params={'type':'movie','tag':'豆瓣高分','sort':'recommend',
                'page_limit':'20','page_start':str(i*20)}
            r=proxy.gethtml(url="https://movie.douban.com/j/search_subjects",headers=self.headers,params=params).json()
            rs=r['subjects']  
            for a in rs:
                film_id=a['id']
                self.run1film(film_id)
        



p=pipeline()
p.run_hot()
