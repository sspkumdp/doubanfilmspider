import requests
import util
from bs4 import BeautifulSoup
import comment
import re
import sql
import user
import header
import proxy
import time

def has_class_and_title(tag):
    return tag.has_attr('title') and tag.has_attr('class')
class comments:

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
    def get_comments_by_film(self,film_id):
        params={'start':'0','limit':'20','status':'P','sort':'new_score'}
        r=proxy.gethtml('https://movie.douban.com/subject/'+str(film_id)+'/comments',self.headers,params)
        if r is None:
            return
        soup=BeautifulSoup(r.content.decode(),'html.parser')
        if soup is None:
            return

        tot=0
        cmt_tab=soup.find('ul',{'class':'fleft CommentTabs'})
        if cmt_tab:
            cmt_tab_span=cmt_tab.find('span')
            if cmt_tab_span:
                txtr=re.search(r'(\d+)',cmt_tab_span.get_text())
                if txtr:
                    tot=int(txtr.group(1))
        #限制一下条数防止爬的太多爬不完
        if tot>util.COMMENT_MAX:
            tot=util.COMMENT_MAX
        
        for i in range(0,int(tot/20)+1):
            params={'start':str(i*20),'limit':'20','status':'P','sort':'new_score'}
            r=proxy.gethtml(url='https://movie.douban.com/subject/'+str(film_id)+'/comments',params=params,headers=self.headers)
            if r is None:
                continue
            soup=BeautifulSoup(r.content.decode(),'html.parser')
            if soup is None:
                continue

            cmts=soup.find_all('div',attrs={'class':'comment-item'})
            if cmts is None:
                continue
            for cmt in cmts:
                c=comment.comment()
                c.comment_id=cmt.get('data-cid')
                #<span class="votes vote-count">1042</span>

                sf=cmt.find('span',attrs={'class':'votes vote-count'})
                if sf:
                    c.comment_useful=sf.get_text()
                ci=cmt.find('span',{'class':'comment-info'})
                if ci:
                    un=ci.find('a')
                    if un:
                        c.user_name=un.get_text()
                        c.user_url=un.get('href')

                urla=re.sub(r'\/$','',c.user_url).split('/')
                if len(urla)>1:
                    c.user_id=urla[-1]

                dbusers=sql.get_user_byid(c.user_id)
                if len(dbusers)==0:
                    new_user=user.user()
                    new_user.user_id=c.user_id
                    new_user.user_name=c.user_name
                    new_user.user_url=c.user_url

                    new_user.get_user_info(new_user.user_url)
                    dbusers=sql.get_user_byid(new_user.user_id)
                    if len(dbusers)==0:
                        sql.save_user(new_user)
                    if new_user.visible=='0':
                        sql.update_user_spider(new_user.user_id)
                

                #<span title="力荐" class="allstar50 rating"></span>
                if ci:
                    star=ci.find('span',{'class':re.compile('allstar')})
                    if star:
                        c.star=str(int(star.get('class')[0].replace('allstar',''))/10)
                    
                    sf=ci.find('span',{'class':'comment-time'})
                    if sf:
                        c.comment_time=sf.get_text().strip()
                
                sf=cmt.find('p',{'class':'comment-content'})
                if sf:
                    sfs=sf.find('span')
                    if sfs:
                        c.comment_content=sfs.get_text()

                c.film_id=film_id
                dbcmts=sql.get_comment_byid(c.comment_id)
                if len(dbcmts)==0:
                    sql.save_comment(c)
                print(c)
                

'''
cmts=comments()
cmts.get_comments_by_film(25907124)
'''