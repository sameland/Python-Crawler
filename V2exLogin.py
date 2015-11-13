import urllib,urllib2,cookielib,re

class v2exLogin:
    cookie_handler = None
    username = None
    password = None
    cookie = None
    cookie_handler = None
    opener = None
    host = None
    login_url = None

    def __init__(self):
        self.username = 'XXX'
        self.password = 'XXX'
        self.host = "https://www.v2ex.com"
        self.login_url = self.host + "/signin"
        self.cookie = cookielib.CookieJar()
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookie_handler)
        urllib2.install_opener(self.opener)

    def get_once(self):
        req = urllib2.Request(self.login_url)
        contents = self.opener.open(req)
        des = r'value="(.*)" name="once"'
        pattern = re.compile(des)
        result = pattern.findall(contents)
        return result[0]

    def get_data(self):
        data = {'u':self.username,'p':self.password,'once':self.get_once(),'next':'/'}
        return urllib.urlencode(data)

    def get_headers(self):
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
           'Content-Type': 'application/x-www-form-urlencoded','Origin':self.host,'Referer': 'https://www.v2ex.com/signin',
           'Host': 'www.v2ex.com','Accept-Encoding': 'gzip'}
        return headers

    def request_login(self):
        req = urllib2.Request(self.login_url,self.get_data(),self.get_headers())
        opener = urllib2.build_opener(self.cookie_handler)
        opener.open(req)

    def finish_daily_mission(self):
        contents = urllib2.urlopen(self.host+"/mission/daily")
        contents = contents.read()
        des = r'location.href = \'(.*)\';'
        pattern = re.compile(des)
        result = pattern.findall(contents)
        url = self.host + result[0]
        contents = urllib2.urlopen(url)
        print(contents)

    def main(self):
        self.request_login()
        self.finish_daily_mission()


if __name__ == '__main__':
    login = v2exLogin()
    login.main()
