#--coding:utf-8--
import os
import re
import sys
import urllib.parse
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

SERVER = 'https://www.biqugex.com/'
SEARCH = 'https://so.biqusoso.com/s.php?siteid=biqugex.com&q=%s'

# 书籍下载目录
BOOKPATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'download')


# 获取章节集合
def getCatalogues(_url):
    req = requests.get(url=_url)
    html = req.text
    div_bf = BeautifulSoup(html, 'lxml')

    _book_name = div_bf.select_one('.book > .info > h2').string

    print('_book_name->%s' % _book_name)

    dd_list = div_bf.select('.listmain > dl > dt')[1].find_next_siblings()

    result_a_list = {}
    i = 0
    for item in dd_list:
        catalog_name = item.select_one('a').text
        catalog_url = SERVER + item.select_one('a').get('href')

        i += 1
        result_a_list[i] = {}
        result_a_list[i]['catalog_name'] = catalog_name
        result_a_list[i]['catalog_url'] = catalog_url
        result_a_list[i]['catalog_id'] = catalog_url.split('/')[-1].split('.')[0]

    return _book_name, result_a_list


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


def searchBook(book_name):
    searchUrl = SEARCH % urllib.parse.quote(book_name.encode('gb2312'))
    print('searchUrl->%s' % searchUrl)
    req = requests.get(url=searchUrl)
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    a_list = bf.select('.search-list > ul >li')[1:]

    book_dict = {}
    for item in a_list:
        i = int(item.select_one('.s1').text)
        href = item.select_one('.s2 > a').get('href')
        book_dict[i] = {}
        book_dict[i]['name'] = item.select_one('.s2 > a').text
        book_dict[i]['author'] = item.select_one('.s4').text
        book_dict[i]['url'] = href
        book_dict[i]['urlid'] = href.split('/')[-1:][0]
    return book_dict


def genSearchBookUrl(search_result_url):
    bq_id = search_result_url.split('/')[-1]
    id = str(bq_id)
    id1 = id[0:len(id) - 3]
    url_result = '%s/%s_%s' % (SERVER, id1, id)
    return url_result


if __name__ == "__main__":
    # print(re.match(r'\d{1,3}', 'http://www.biqukan.com/18_18056/6412383.html'))

    catalog_url = 'http://www.biqukan.com/2_2722'  #genSearchBookUrl(book_id)

    print('catalog_url->%s' % catalog_url)

    _book_name, a_list = getCatalogues(catalog_url)

    k = 0
    count = len(a_list)
    for key, value in a_list.items():
        k += 1
        print('item->%s' % value)
        chapter_title = downBook(_book_name, value['catalog_url'])
        print('已下载 %s' % chapter_title)
        sys.stdout.write("已下载:%.2f%%" % float(k / count * 100) + '\r')
        sys.stdout.flush()

    print('全书下载完成！')

    # # test
    # href = 'http://www.biqukan.com/book/goto/id/34459'
    # print(href.split('/')[-1:][0])

    # bn = input('请输入您要下载的书籍名称：')

    # book_dict = searchBook(bn.strip())

    # select_result = {}
    # if len(book_dict) == 0:
    #     print('未查询到书籍')
    #     sys.exit()
    # elif len(book_dict) == 1:
    #     select_result = book_dict[1]
    # else:
    #     for key, value in book_dict.items():
    #         print('%s.%s' % (key, value['name']))
    #     select_book_idx = input('请选择要下载的书籍：')
    #     select_result = book_dict[int(select_book_idx)]

    # print('select_result->%s' % select_result)
    # url_result = ''
    # if select_result is None:
    #     print('您选择的书籍不存在')
    #     sys.exit()
    # else:
    #     print('您选择的书籍为->%s' % select_result['name'])
    #     url_result = genSearchBookUrl(select_result['url'])
    #     print('url_result->%s' % url_result)

    # _book_name, a_list = getCatalogues(url_result)

    # k = 0
    # count = len(a_list)
    # for item in a_list:
    #     k += 1
    #     chapter_title = downBook(_book_name, item)
    #     print('已下载 %s' % chapter_title)
    #     sys.stdout.write("已下载:%.2f%%" % float(k / count * 100) + '\r')
    #     sys.stdout.flush()

    # print('全书下载完成！')
