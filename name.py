# Author : ZhangTong
import requests
import random
import pymysql
from pyquery import PyQuery as pq
from multiprocessing.pool import Pool
from config import *

def ua():
    ua = ['Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
          'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
          ]
    return random.choice(ua)

def download(url):
    headers = {
               'User-Agent': ua()
    }

    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        else:
            print('请求失败')
            return download(url)
    except:
        return download(url)

def parse_first(text):
    allHrefs = []
    doc = pq(text)
    a = doc('.col-xs-12 .btn')
    for i in a:
        href = 'http:%s' % i.attrib['href']
        href = structure_href(href)
        allHrefs.extend(href)
    return allHrefs

def structure_href(href):
    hrefs = []
    for i in range(1, 11):
        boys = href.split('_')[0] + '/boys_%d.html' % i
        hrefs.append(boys)
    for i in range(1, 11):
        girls = href.split('_')[0] + '/girls_%d.html' % i
        hrefs.append(girls)
    return hrefs

def first(url):
    try:
        text = download(url)
        hrefs = parse_first(text)
        return hrefs
    except Exception as e:
        print(e)

def parse_second(text):
    doc = pq(text)
    # title = doc('title').text()
    # print(title)
    a = doc('.col-xs-12 .btn-link')
    for i in a:
        name = i.text
        yield name

def save(name):
    sql = 'insert into names(name) values(%s)'
    try:
        cursor.execute(sql, (name,))
    except:
        db.rollback()
        print('=' * 100)
    else:
        db.commit()
        print(name)


def second(href):
    text = download(href)
    names = parse_second(text)
    for name in names:
        save(name)

def main(url):
    # hrefs = first(url)
    # for href in hrefs:
    #     second(href)
    second(url)

if __name__ == '__main__':
    url = 'http://www.resgain.net/xmdq.html'
    # main(url)
    hrefs = first(url)
    pool = Pool()
    pool.map(main,hrefs)
    pool.close()
    pool.join()
