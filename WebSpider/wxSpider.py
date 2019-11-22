#--coding:utf-8--
import os
import re
import sys
import urllib.parse
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

SERVER = 'https://mp.weixin.qq.com/s/7MI-WNBePwK9WNHGz6DnNA'

BOOKPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'download')


def downBook(_book_name, a_href):
    req = requests.get(url=a_href)
    html = req.text.encode('iso-8859-1')
    bf = BeautifulSoup(html, 'lxml')

    # 章节标题
    chapter_title = bf.select_one('.reader > .content > h1').text

    # 正则表达式拆分文中url，(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]
    content = re.split(r'[(](https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|][)]',
                       bf.select_one('#content').text.replace('\xa0' * 8, '\n    '))[0]

    # 如果当前目录不存在文件夹，则新建一个文件夹
    book_path = os.path.join(BOOKPATH, _book_name + '.txt')

    if not os.path.isdir(BOOKPATH):
        os.makedirs(BOOKPATH)

    if not os.path.isfile(book_path):
        with open(book_path, 'w', encoding='utf-8') as f:
            f.writelines('\n')
            f.writelines('\t' + _book_name)

    with open(book_path, 'a', encoding='utf-8') as f:
        f.write('\n\n\n\t')
        f.write(chapter_title)
        f.write('\n')
        f.write(content)

    return chapter_title


def query(_url, _result):
    req = requests.get(url=SERVER)
    html = req.text
    bf = BeautifulSoup(html, 'lxml')

    a_list = bf.select('a[data-itemshowtype="0"]')[0:-2]

    for a in a_list:
        _result[a.text] = a['href']

    if (len(_result) < 100):
        return _result
    else:
        query(_url, _result)


if __name__ == "__main__":
    result = {}
    query(SERVER, result)
