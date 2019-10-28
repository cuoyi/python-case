# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    server = 'http://www.biqukan.com'
    target = 'http://www.biqukan.com/1_1094/'
    req = requests.get(url=target)
    html = req.text.encode("iso-8859-1")
    div_bf = BeautifulSoup(html, 'lxml')
    div = div_bf.find_all('div', class_='listmain')[0]
    a_bf = BeautifulSoup(str(div), 'lxml')
    a_list = a_bf.find_all('a')[13:200]
    for item in a_list:
        with open('test.txt', 'a', encoding='utf-8') as f:
            f.write('%s %s\n' % (item.string, server + item.get('href')))
        print(item.string, server + item.get('href'))
