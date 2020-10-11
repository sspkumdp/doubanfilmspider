'''
获取电影信息
'''
import requests
import util
from bs4 import BeautifulSoup

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
    def get_film(self,film_id):
        r=requests.get(url='https://movie.douban.com/subject/'+str(film_id),headers=self.headers)
        soup=BeautifulSoup(r.content.decode(),'html.parser')
        body=soup.body
        
        self.film_id=str(film_id)
        #<span property="v:itemreviewed">姜子牙</span>        
        self.film_name=util.listtostr(body.find_all('span',attrs={'property':'v:itemreviewed'}),'')
        #<a href="/celebrity/1315977/" rel="v:directedBy">程腾</a>
        self.director=util.listtostr(body.find_all('a',attrs={'rel':'v:directedBy'}),"/")
        
        sw=body.find('span',attrs={'class':'pl'},text='编剧')
        self.screenwriter=util.listtostr(sw.find_next_sibling('span').contents,'/')
        #<a href="/celebrity/1384856/" rel="v:starring">郑希</a>
        self.mainactors=util.listtostr(body.find_all('a',attrs={'rel':'v:starring'}),"/")
        #<span property="v:genre">剧情</span>
        self.film_type=util.listtostr(body.find_all('span',attrs={'property':'v:genre'}),'/')

        #<span class="pl">制片国家/地区:</span>
        sw=body.find('span',attrs={'class':'pl'},text='制片国家/地区:')
        self.area=sw.next_sibling.strip()
        

        sw=body.find('span',attrs={'class':'pl'},text='语言:')
        self.lang=sw.next_sibling.strip()
        #<span property="v:initialReleaseDate" content="2020-10-01(中国大陆)">2020-10-01(中国大陆)</span>
        self.film_date=util.listtostr(body.find_all('span',attrs={'property':'v:initialReleaseDate'}),'/')

        #<span property="v:runtime" content="110">110分钟</span>
        self.film_time=util.listtostr(body.find_all('span',attrs={'property':'v:runtime'}),'/')


        #<span class="pl">又名:</span>
        sw=body.find('span',attrs={'class':'pl'},text='又名:')
        self.film_alias=sw.next_sibling.strip()

        #<span class="pl">IMDb链接:</span>
        sw=body.find('span',attrs={'class':'pl'},text='IMDb链接:')
        self.screenwriter=sw.find_next_sibling('a').get_text()

        #<strong class="ll rating_num" property="v:average">7.0</strong>
        self.score=body.find('strong',attrs={'property':'v:average'}).get_text()


        print(self)

        


f=film()
f.get_film(25907124)

