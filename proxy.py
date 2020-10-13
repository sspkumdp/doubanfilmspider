import requests
import time
import util
import random
import agents

PROXY_URL='http://118.190.199.189:5010/get/'
def get1httpproxy():
    js=requests.get(PROXY_URL).json()
    if js:
        p=js.get('proxy')
        return "http://{}".format(p)

def gethtml(url,headers,params):
    agents.get1agent(headers)
    try_time=0
    while True:
        try:
            r=requests.get(url,headers=headers,params=params,proxies={"http":get1httpproxy()},timeout=1)
            time.sleep(util.SLEEP_TIME+random.random()/2)
            return r
        except Exception:
            try_time+=1
            




