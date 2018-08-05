import requests
import re
import json

def get_items(pattern, html):
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actors': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4][5:] if len(item[4])>5 else ''
        }

re_str = re.compile('<dd>.*?>(.*?)</i>.*?-src="(.*?)@.*?alt="(.*?)".*?"star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?tion">(\d)' ,re.S)
url = 'http://maoyan.com/board/4'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Host': 'maoyan.com',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

if __name__ == '__main__':
    with open('movies', 'w') as f:
        for offset in range(10):
            response = requests.get(url+'?offset='+str(offset*10), headers=headers)
            if response.status_code == 200:
                for item in get_items(re_str, response.text):
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
        