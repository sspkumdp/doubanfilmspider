import logging
import time
import logging.handlers


#初始化设置
logging.basicConfig(level = logging.INFO,format='%(asctime)s|%(name)-12s: %(levelname)-8s %(message)s')
#创建
logger = logging.getLogger("zzz")
logger.setLevel(logging.INFO)


handler1=logging.FileHandler("base-log.log")
handler1.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s')
handler1.setFormatter(formatter)

logger.addHandler(handler1)


