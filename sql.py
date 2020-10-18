import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123',
                             db='douban_film',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


#插入电影
def insert_film(film):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `film` (`film_id`,`film_name`,`director`,`screenwriter`,`mainactors`,`film_type`,`area`,`lang`,`film_date`,`film_time`,`film_alias`,`imdb`,`score`,`film_summary`,`spider`) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s,%s, '0')"
        cursor.execute(sql, (film.film_id,film.film_name,film.director,film.screenwriter
            ,film.mainactors,film.film_type,film.area,film.lang,film.film_date,film.film_time
            ,film.film_alias,film.imdb,film.score,film.film_summary))
    connection.commit()

def get_film_byid(film_id):
    with connection.cursor() as cursor:
        sql = "SELECT `film_id`,`spider` FROM `film` where film_id=%s"
        cursor.execute(sql, (film_id))
        return cursor.fetchall()

def get_unspider_film():
    with connection.cursor() as cursor:
        sql = "SELECT `film_id` FROM `film` where spider='0'"
        cursor.execute(sql, ())
        return cursor.fetchall()

def update_film_spider(film_id):
    with connection.cursor() as cursor:
        sql = "update `film` set spider='1' where film_id=%s"
        cursor.execute(sql, (film_id))
    connection.commit()

def update_film_byid(film):
    with connection.cursor() as cursor:
        sql = "update `film` set `film_id`=%s,`film_name`=%s,`director`=%s,`screenwriter`=%s,`mainactors`=%s,`film_type`=%s,`area`=%s,`lang`=%s,`film_date`=%s,`film_time`=%s,`film_alias`=%s,`imdb`=%s,`score`=%s, film_summary=%s where film_id=%s"
        cursor.execute(sql, (film.film_id,film.film_name,film.director,film.screenwriter
            ,film.mainactors,film.film_type,film.area,film.lang,film.film_date,film.film_time
            ,film.film_alias,film.imdb,film.score,film.film_summary,film.film_id))
    connection.commit()


def save_comment(comment):
    with connection.cursor() as cursor:
        sql = "insert into `comment` (`comment_id`,`user_id`,`film_id`,`star`,`comment_time`,`comment_useful`,`comment_content`,`update_time`) values(%s,%s,%s,%s,%s,%s,%s,now())"
        cursor.execute(sql,(comment.comment_id,comment.user_id,comment.film_id,comment.star,comment.comment_time,comment.comment_useful,comment.comment_content))
    connection.commit()

def get_comment_byid(comment_id):
    with connection.cursor() as cursor:
        sql = "SELECT `comment_id` FROM `comment` where comment_id=%s"
        cursor.execute(sql, (comment_id))
        return cursor.fetchall()


def save_actor(act):
    with connection.cursor() as cursor:
        sql="insert into `actor` (`actor_id`,`main_works`,`actor_name`,`gender`,`xingzuo`,`birthday`,`birtharea`,`occupation`,`more_name`,`more_foreign_name`,`imdb_id`,`web_url`,`update_time`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"
        cursor.execute(sql,(act.actor_id,act.main_works,act.actor_name,act.gender,act.xingzuo,act.birthday,act.birtharea,act.occupation,act.more_name,act.more_foreign_name,act.imdb_id,act.web_url))
    connection.commit()

def get_actor_byid(actor_id):
    with connection.cursor() as cursor:
        sql = "SELECT `actor_id` FROM `actor` where actor_id=%s"
        cursor.execute(sql, (actor_id))
        return cursor.fetchall()

def save_actor_film(actor_id,film_id,role):
    with connection.cursor() as cursor:
        sql="insert into `actor_film` (`actor_id`,`film_id`,`role`) values(%s,%s,%s)"
        cursor.execute(sql,(actor_id,film_id,role))
    connection.commit()

def get_actor_film_byid(actor_id,film_id):
    with connection.cursor() as cursor:
        sql = "SELECT `actor_id` FROM `actor_film` where actor_id=%s and film_id=%s"
        cursor.execute(sql, (actor_id,film_id))
        return cursor.fetchall()

def save_user(user):
    with connection.cursor() as cursor:
        sql="insert into `user`(`user_id`,`user_name`,`user_url`,`user_area`,`user_time`,`user_info`,`viewed_count`,`wish_count`,`visible`,`spider`,`update_time`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,'0',now())"
        cursor.execute(sql,(user.user_id,user.user_name,user.user_url,user.user_area,user.user_time,user.user_info,user.viewed_count,user.wish_count,user.visible))
    connection.commit()

def get_user_byid(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT `user_id` FROM `user` where user_id=%s"
        cursor.execute(sql, (user_id))
        return cursor.fetchall()


def get_unspider_user():
    with connection.cursor() as cursor:
        sql = "SELECT `user_id`,`user_url` FROM `user` where spider='0'"
        cursor.execute(sql, ())
        return cursor.fetchall()

def update_user_spider(user_id):
    with connection.cursor() as cursor:
        sql = "update `user` set spider='1' where user_id=%s"
        cursor.execute(sql, (user_id))
    connection.commit()
