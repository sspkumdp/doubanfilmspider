
'''
# -*- coding: utf-8 -*-
from snownlp import SnowNLP
s1 = SnowNLP(u"这本书质量真不太好！")
print("SnowNLP:")
print(" ".join(s1.words))

import jieba
s2 = jieba.cut(u"这本书质量真不太好！", cut_all=False)
print("jieba:")
print(" ".join(s2))
'''


from snownlp import SnowNLP
import os

rootdir = '/Users/yumiko/Desktop/comment'
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
for i in list:
    # print(i)
    f = open(os.path.join(rootdir, i), 'r', encoding='UTF-8')
    file = os.path.join(rootdir, i)
    print(f)
    if  file.endswith('.rtf'):
        list = f.readlines()
        sentimentslist = []
        sum = 0
        count = 0
        for i in list:
            s = SnowNLP(i)
            # print s.sentiments
            #print(s.sentiments)
            sum+=(s.sentiments)
            count+=1
        print(sum/count)

'''
plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01), facecolor='g')
plt.xlabel('Sentiments Probability')
plt.ylabel('Quantity')
plt.title('Analysis of Sentiments')
plt.show()
'''

