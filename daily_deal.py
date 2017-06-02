#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chunmato'

import urllib2
from bs4 import BeautifulSoup

import re


def fetch_page(url):
   # url = "http://www.tmsf.com/daily.htm"
    try:
        req = urllib2.Request(url, headers = {'User-Agent': 'Magic Browser'})
        page = urllib2.urlopen(req)
        data = page.read()
        return data
    except urllib2.HTTPError, e:
        print "error " + str(e.errno) + " when read " + url
        with open('errlog.log', 'a') as ef:
            ef.write(url + '\n')
        return ""


def parse_first_hand_text(text):
    pattern = '杭州(.*)排名第二'.decode('utf8')
    m = re.search(pattern, text.decode('utf8'))
    if m is None:
        return []
    t = m.group(0)
    res = []
    pattern_places = ['主城区签约(\d+)套', '萧山(\d+)套', '余杭(\d+)套', '富阳(\d+)套', '桐庐(\d+)套', '建德(\d+)套', '淳安(\d+)套', '临安(\d+)套']
    # main city
    for p in pattern_places:
        pat = p.decode('utf8')
        m = re.search(pat, t)
        if m is None:
            res.append(0)
        else:
            res.append(int(m.group(1)))

    return res



if __name__ == "__main__":
    page = fetch_page("http://www.tmsf.com/daily.htm")
    soup = BeautifulSoup(page)
    myCont2 = soup.find(id="myCont2")
    print(myCont2)
    #print page
