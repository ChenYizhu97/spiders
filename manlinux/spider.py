import requests
from pyquery import PyQuery 
import re
import time
import random
import json

url = 'http://man.linuxde.net'
re_subclass = re.compile('.*/sub/(.*)')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie':'_zap=74e71e40-3350-411a-b965-b121a52cf367; d_c0="AICkLsa__w2PTtpfp5Hroh2Pt57zlTxpq8I=|1533281332"; q_c1=8c6f6a9c4e6b48d291562c1bc93396da|1533281333000|1533281333000',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'cache-control': 'max-age=0'
}
def get_subclass_urls(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        html = PyQuery(res.text)
        items = html.find('#tags-list dd a').items()
        for item in items:
            yield item('a').attr('href')
    else: 
        return []

def get_command_urls(subclass_url):
    res = requests.get(subclass_url, headers=headers)
    if res.status_code == 200:
        html = PyQuery(res.text)
        items = html.find('#arcs-list li').items()
        for item in items:
            yield item('a').attr('href')
    else:
        return []



def get_command(command_url):
    res = requests.get(command_url, headers=headers)
    command = {}
    if res.status_code == 200:
        html = PyQuery(res.text)
        command['title'] = html('#title h1').text()
        infos = html('#arc-body')
        for item in infos.find('h3').items():
            command[item.text()] = item.next().text()
        return command
    else:
        return []
        


if __name__ == '__main__':
    commands = {}
    index = 0
    with open('commandlinux', 'w', encoding='utf-8') as f:
        for subclass_url in get_subclass_urls(url):
            subclass = re.match(re_subclass, subclass_url).group(1)
            for command_url in get_command_urls(subclass_url):
                command = get_command(command_url)
                command['class'] = subclass
                print('\n',index,'\n',command)
                f.write(json.dumps(command, ensure_ascii=False) + '\n')
                time.sleep(random.randint(0, 5))
                index +=1