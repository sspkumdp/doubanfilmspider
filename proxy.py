import requests
import time
import util
import random
import agents
import time


PROXY_URL='http://localhost:5010/get/'

XIAOXIANG='https://api.xiaoxiangdaili.com/ip/get'
XIAOXIANGP={'appKey':'yourkey','appSecret':'yourpassword'}
XXIP='0.0.0.0'
now=0
def get1httpproxy():
    js=requests.get(PROXY_URL).json()
    if js:
        p=js.get('proxy')
        return p
    

def get1xxproxy():
    global now
    global XXIP
    nt=time.time()
    if nt-now>20:
        js=requests.get(XIAOXIANG,params=XIAOXIANGP).json()
        if js['code']==200:
            jsd=js['data'][0]
            XXIP=jsd['ip']+":"+str(jsd['port'])
        now=nt
    print(XXIP)
    return XXIP

    
    

def gethtml(url,headers,params):
    agents.get1agent(headers)
    try_time=10
    while True:
        print(try_time)
        print(url)
        if try_time<0:
            needt=now+20-time.time()
            if needt>0:
                time.sleep(needt+1)
            try_time=10
            continue
        try:
            ip=get1xxproxy()
            r=requests.get(url,headers=headers,params=params,proxies={"http":"http://{}".format(ip),"https":"https://{}".format(ip)},timeout=3)
            time.sleep(random.random()/3)
            return r
        except Exception:
            try_time-=1

'''
get1xxproxy()
'''
