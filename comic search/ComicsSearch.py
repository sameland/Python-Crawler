# -*- coding: utf-8 -*-
# 读取目录下的list.txt内的漫画列表,获取极速漫画的每日更新
__author__ = 'sameland'
import time, urllib2, re, cookielib


class ComicsSearch:
    host = "http://www.1kkk.com"
    newest_page = "http://www.1kkk.com/manhua-new"
    name_re = r'<br />([\x21-\xff]+[\x20,\x2f]*[\x21-\xff]+)</a><span class="lj_h1">'
    time_re = r'</span><br />([\x80-\xff,\s,a-z,0-9,A-Z,-]+)<span class="flowtag">'
    url_re = r'<span class="lj_h1"><a href="([\x21-\x7e]+[\x5f]*[\x21-\x7e]+)">'
    comics_list = None
    url_result = None
    time_result = None
    name_result = None
    content = None
    opener = None
    curr_time = None
    page = "-p"
    count = 2
    isContinue = True
    start_check = False

    def __init__(self):
        file = open('list.txt', 'r')
        file_content = file.read().decode('gbk').encode('utf-8')
        self.comics_list = file_content.split('，')
        file.close()
        self.curr_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.yes_time = time.strftime('%Y-%m-%d', time.localtime(time.time() - 1 * 24 * 3600))
        cookie = cookielib.CookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(cookie_handler)
        urllib2.install_opener(self.opener)

    def request_content(self, url):
        content = self.opener.open(url)
        content = content.read()
        name_pattern = re.compile(self.name_re)
        self.name_result = name_pattern.findall(content)
        print self.name_result.__len__()
        time_pattern = re.compile(self.time_re)
        self.time_result = time_pattern.findall(content)
        url_pattern = re.compile(self.url_re)
        self.url_result = url_pattern.findall(content)

    def filter_comics(self):
        while self.isContinue:
            for idx, val in enumerate(self.time_result):
                tmp_name = self.name_result[idx]
                if val.__contains__(self.curr_time) or val.__contains__(self.yes_time):
                    print self.name_result[idx]
                    if tmp_name in self.comics_list:
                        print self.host + self.url_result[idx]
                    self.start_check = True
                else:
                    if self.start_check:
                        self.isContinue = False
                        break
                if idx == self.url_result.__len__() - 1:
                    url = self.newest_page + self.page + str(self.count)
                    self.request_content(url)
                    self.count += 1
                    # else:
                    #     self.isContinue = False
                    #     break

    def main(self):
        self.request_content(self.newest_page)
        self.filter_comics()


if __name__ == '__main__':
    comcis = ComicsSearch()
    comcis.main()
