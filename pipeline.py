import sql
import film
import comments_by_film
import user
import time
class pipeline:
    def run1film(self,film_id):
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
        dbflms=sql.get_film_byid(film_id)
        if len(dbflms)>0:
            if dbflms[0]['spider']=='1':
                self.run_unspider()
                return
        
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


        
        



p=pipeline()
p.run(25907124)
