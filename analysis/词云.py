

#coding=utf-8
import matplotlib
import matplotlib.pyplot as plt
from imageio import imread
from wordcloud import WordCloud, STOPWORDS
import jieba, codecs
from collections import Counter

text = codecs.open('/Users/yumiko/Desktop/comment/children.rtf', 'r', encoding='utf-8').read()

wordlist=jieba.cut(text)
wsp=" ".join(wordlist)

stopdict=set(STOPWORDS)
def make_stopdict():
    f = open("/Users/yumiko/Desktop/chineseStopWords.txt", "r") #网上下载来的停止词文本，近2000个，可以自己往里面添加
    lines = f.readlines()
    for l in lines:
        stopdict.add(l.strip())
    f.close()
make_stopdict()

bg_pic = imread('/Users/yumiko/Desktop/panda.jpeg')
wc = WordCloud(
    font_path='/Applications/Microsoft PowerPoint.app.installBackup/Contents/Resources/DFonts/Fangsong.ttf', #指定中文字体
    background_color='white',  # 设置背景颜色
    max_words=3000,  # 设置最大显示的字数
    mask=bg_pic,  # 设置背景图片
    max_font_size=200,  # 设置字体最大值
    random_state=20,  # 设置多少种随机状态，即多少种配色
    stopwords=stopdict,
    scale=4
).generate(wsp)
#wc.generate_from_frequencies(dict(word))  # 生成词云

wc.to_file('result.jpg')
# show
plt.imshow(wc)
plt.axis("off")
plt.show()
'''
plt.axis("off")
plt.figure()
plt.imshow(bg_pic, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
'''