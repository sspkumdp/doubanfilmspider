import requests
import proxy
headers={

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
            }
r=proxy.gethtml(url="https://movie.douban.com",headers=headers,params={})
print(r.content.decode())