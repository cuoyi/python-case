# -*- coding:UTF-8 -*-

import os
import re

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # target = 'http://www.biqukan.com/1_1094/5403177.html'
    target = 'https://www.biqukan.com/2_2718/1056393.html'
    req = requests.get(url=target)
    html = req.text.encode('iso-8859-1')
    bf = BeautifulSoup(html, 'lxml')
    title = bf.find_all('h1')[0].text
    print(title)
    content = str(
        bf.find_all('div', class_='showtxt')[0].text.replace(
            '\xa0' * 8, '\n    ')).split('[笔趣看')[0]

    # 如果文件不存在，则新建一个文件
    if not os.path.exists('test.txt'):
        with open(title + '.txt', 'w', encoding='utf-8') as f:
            f.write("\n    " + title + "\n")
            f.write(content)
    # print(txt.text.replace('\xa0' * 8, '\n    '))
