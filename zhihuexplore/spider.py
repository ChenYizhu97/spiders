import requests
from pyquery import PyQuery
import codecs

url = 'https://www.zhihu.com/explore'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie':'_zap=74e71e40-3350-411a-b965-b121a52cf367; d_c0="AICkLsa__w2PTtpfp5Hroh2Pt57zlTxpq8I=|1533281332"; q_c1=8c6f6a9c4e6b48d291562c1bc93396da|1533281333000|1533281333000',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'cache-control': 'max-age=0'
}

htmldoc = requests.get(url, headers=headers).text
pyquery = PyQuery(htmldoc)
items = pyquery('.explore-tab .feed-item').items()

with codecs.open('answers', 'w', 'utf-8') as f:
    for (index, item) in enumerate(items):  
        question = item.find('.question_link').text()
        author = item.find('.author-link').text()
        content = PyQuery(item.find('.content').html()).text()
        index = str(index)
        f.write('question:' + index + ' '*3 + question + '\n')
        f.write('author:' + index + ' '*3 + author + '\n')
        f.write('content:' + index + ' '*3 + content + '\n')
        f.write('=' * 50 + '\n')
