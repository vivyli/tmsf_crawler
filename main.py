#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chunmato'

import urllib2
from datetime import date
from datetime import timedelta
import re


def fetch_page_date(d):
    url = "http://www.tmsf.com/upload/report/mrhqbb/"+d.strftime("%Y%m%d")+"/index.html"
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
    pattern_places = ['主城区签约(\d+)套', '萧山(\d+)套', '余杭(\d+)套', '富阳(\d+)套', '桐庐(\d+)套', '建德(\d+)套', '淳安(\d+)套', '临安(\d+)套', '大江东(\d+)套', '二手房共签约(\d+)套']
    # main city
    for p in pattern_places:
        pat = p.decode('utf8')
        m = re.search(pat, t)
        if m is None:
            res.append(0)
        else:
            res.append(int(m.group(1)))

    return res


def get_write_string(sold_list, dt):
    text = dt.strftime("%Y-%m-%d") + "," + \
        str(sold_list[0]) + "," + \
        str(sold_list[1]) + "," + \
        str(sold_list[2]) + "," + \
        str(sold_list[3]) + "," + \
        str(sold_list[4]) + "," + \
        str(sold_list[5]) + "," + \
        str(sold_list[6]) + "," + \
        str(sold_list[7])
    return text

if __name__ == "__main__":
    cur_day = date(2016, 8, 3) #date(2013, 2, 16)
    end_day = date.today()
    with open('tmsf.csv', 'a') as f:
    	title = '时间,主城区,萧山,余杭,富阳，桐庐,建德,淳安,临安,大江东,二手房'
	f.write(title +'\n')
        while cur_day != end_day:
            page = fetch_page_date(cur_day)
            #retrieve data
            if len(page) > 0:
                sold_list = parse_first_hand_text(page)
                print sold_list
                if len(sold_list) > 0:
                    line = get_write_string(sold_list, cur_day)
                    print "writing: " + line
                    f.write(line + '\n')
                else:
                    with open('errlog.log', 'a') as ef:
                        ef.write('http://www.tmsf.com/upload/report/mrhqbb/'+cur_day.strftime("%Y%m%d") +
                                 '/index.html' + '\n')
            cur_day = cur_day + timedelta(days=1)
