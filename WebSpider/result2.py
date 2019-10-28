import os
import sys
import urllib.parse
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

SERVER = 'http://www.biqukan.com'
TARGET = 'http://www.biqukan.com/1_1094/'
SEARCH = 'https://so.biqusoso.com/s.php?siteid=biqukan.com&q=%s'

BOOKPATH = 'E:\\work\\note\\Python\\WebSpider\\book'


# 获取章节集合
def getCatalogues(_url):
    req = requests.get(url=_url)
    html = req.text
    div_bf = BeautifulSoup(html, 'lxml')

    _book_name = div_bf.find('div', class_='info').findChildren('h2')[0].text

    print('_book_name->%s' % _book_name)

    div = div_bf.find_all('div', class_='listmain')[0]
    a_bf = BeautifulSoup(str(div), 'lxml')
    result_a_list = []
    a_list = a_bf.find_all('a')[13:]
    for item in a_list:
        # downBook(SERVER + item.get('href'))
        result_a_list.append(SERVER + item.get('href'))
    return _book_name, result_a_list


def downBook(_book_name, a_href):
    req = requests.get(url=a_href)
    html = req.text.encode('iso-8859-1')
    bf = BeautifulSoup(html, 'lxml')
    title = bf.find_all('h1')[0].text
    _path = os.path.join(BOOKPATH, _book_name + '.txt')
    content = str(
        bf.find_all('div', class_='showtxt')[0].text.replace(
            '\xa0' * 8, '\n    ')).split('[笔趣看')[0]
    # 如果文件不存在，则新建一个文件
    # if not os.path.exists(_path):
    with open(_path, 'a', encoding='utf-8') as f:
        f.writelines('\n\n\n\t')
        f.write(title)
        f.writelines('\n\n')
        f.write(content)


def searchBook(book_name):
    searchUrl = SEARCH % urllib.parse.quote(book_name.encode('gb2312'))
    print('searchUrl->%s' % searchUrl)
    req = requests.get(url=searchUrl)
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    a_list = bf.find_all('a')
    book_dict = {}
    i = 0
    print("a_list->%s" % a_list)
    for item in a_list:
        i += 1
        book_dict[i] = {}
        book_dict[i]['name'] = item.text
        book_dict[i]['url'] = item.get('href')
    print(book_dict)
    return book_dict


def genSearchBookUrl(search_result_url):
    l = search_result_url.split('/')
    id = str(l[len(l) - 1])
    id1 = id[0:len(id) - 3]
    # id2 = id[len(id) - 3:len(id)]
    url_result = '%s/%s_%s' % (SERVER, id1, id)
    print(url_result)
    return url_result


if __name__ == "__main__":
    book_dict = searchBook('遮天')
    print('book_dict->%s' % book_dict)

    i = 0
    for key, value in book_dict.items():
        i += 1
        print('%s.%s' % (key, value['name']))
    select_book_idx = input('请选择要下载的书籍：')
    select_result = book_dict[int(select_book_idx)]
    print('select_result->%s' % select_result)
    url_result = ''
    if select_result is None:
        print('您选择的书籍不存在')
    else:
        print('您选择的书籍为->%s' % select_result['name'])
        url_result = genSearchBookUrl(book_dict[int(select_book_idx)]['url'])
        print('url_result->%s' % url_result)

    _book_name, a_list = getCatalogues(url_result)

    k = 0
    count = len(a_list)
    for item in a_list:
        k += 1
        # print('_book_name->%s \nitem->%s' % (_book_name, item))
        downBook(_book_name, item)
        sys.stdout.write("已下载:%.3f%%" % float(k / count * 100) + '\r')
        sys.stdout.flush()

    print('全书下载完成！')
