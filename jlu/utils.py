'''
Generate a url to JiLin University VPN
'''
import urllib.parse
import urllib3
import chardet

key = [0x6f, 0x68, 0xde, 0x3, 0xb8, 0xaf, 0xf7, 0xcf, 0xe1, 0x97, 0x16, 0x33, 0x7, 0xca, 0xbc, 0xaa, 0xc6]
meaningless_bullshit = '77726476706e69737468656265737421'


def generate(origin: str):
    info = urllib.parse.urlparse(origin)
    host = info.hostname
    print(info)
    print('Original Host Name : %s' % host)
    tmp = []
    for i in range(len(host)):
        tmp.append(hex(ord(host[i]) ^ 0xff ^ key[i])[2:])
    for index, t in enumerate(tmp):
        if len(t) < 2:
            tmp[index] = '0' + t
    print(tmp)
    text = ''.join(tmp)
    print(text)
    full = 'https://vpns.jlu.edu.cn/' + info.scheme + '/' + meaningless_bullshit + text + info.path
    if info.params:
        full += '?' + info.params
    if info.query:
        full += '?' + info.query
    if info.fragment:
        full += '#' + info.fragment
    return full


class Logger(object):
    __instance = None
    __initFlag = False
    __isClose = False
    __method = "console"
    __filePointer = None

    def __write(self, text):
        if self.__isClose is False:
            if self.__method == "console":
                print(text)
            elif self.__method == "file":
                self.__filePointer.write(text)

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, method="console"):
        if Logger.__initFlag:
            return
        if method == "" or method == " " or method != "file":
            pass
        else:
            self.__method = str(method).lower()
        if self.__method == "file":
            self.__filePointer = open("./announcebot.log", 'a', encoding='utf-8')
        Logger.__initflag = True

    def setMethod(self, method):
        self.__method = str(method).lower()
        if self.__method == "file" and self.__filePointer == None:
            self.__filePointer = open("./announcebot.log", 'a', encoding='utf-8')

    def error(self, text):
        self.__write("\033[0;31;40m[ERROR] " + str(text) + "\033[0m")
        return

    def notice(self, text):
        self.__write("\033[0;33;40m[NOTICE] " + str(text) + "\033[0m")
        return

    def info(self, text):
        self.__write("\033[0;32;40m[INFO] " + str(text) + "\033[0m")
        return


from lxml import etree
import datetime, operator, functools, requests
from urllib import parse


class GetAnnounce(object):
    __domain = "https://oa.jlu.edu.cn/"
    __direct = "defaultroot/"
    __list = "PortalInformation!jldxList.action?channelId=179577"
    __cacheList = []
    __cacheContent = []
    __linkBaseUrl = "rd/download/BASEEncoderAjax.jsp"
    __downloadBaseUrl = "rd/download/attachdownload.jsp?res="
    __header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    __obj = None
    __initFlag = False
    __max = 31
    __logger = None

    def __testHttp(self, target):
        try:
            self.__logger.info("正在测试网络连通...")
            return requests.get(target)
        except:
            return False

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = super().__new__(cls)
        return cls.__obj

    def __init__(self, text=""):
        self.__logger = Logger()
        if self.__initFlag is False:
            if text == "" or text == " ":
                self.__domain = "https://sh.evyde.xyz:6565/"
            else:
                self.__domain = text
            if self.__testHttp(self.__domain):
                self.__logger.notice("Http连接成功！")
                self.__logger.info("目标地址：" + self.__domain)

            else:
                self.__logger.error("连接错误！请检查网络连接！")
                raise Exception("NetworkError")
        self.__initFlag = True

    def __cmpDatetime(o, a, b):
        aDatetime = datetime.datetime.strptime(a['time'], '%Y年%m月%d日 %H:%M\xa0\xa0')
        bDatetime = datetime.datetime.strptime(b['time'], '%Y年%m月%d日 %H:%M\xa0\xa0')

        # 比较进行到这里说明a, b都是置顶或非置顶，则按时间进行排序
        if aDatetime > bDatetime:
            return -1
        elif aDatetime < bDatetime:
            return 1
        else:
            return 0

    def __cmpIsTop(o, a, b):
        isATop = a['top']
        isBTop = b['top']
        if isATop == "[置顶]" and isBTop == "":
            return -1
        elif isATop == "" and isBTop == "[置顶]":
            return 1
        else:
            return 0

    def __cacheSort(self, sortTarget):
        # 按时间排序
        sortTarget.sort(key=functools.cmp_to_key(self.__cmpDatetime))
        # 按是否置顶排序
        sortTarget.sort(key=functools.cmp_to_key(self.__cmpIsTop))
        return sortTarget

    def createListCache(self):
        self.__cacheList = []
        self.__cacheContent = []
        self.__logger.info("正在获取主页内容...")
        html = requests.get(self.__domain + self.__direct + self.__list).text
        self.__logger.notice("获取成功！")
        data = etree.HTML(html)
        for i in range(1, self.__max):
            time = data.xpath('//*[@id="itemContainer"]/div[%d]/span/text()' % i)
            href = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/@href' % i)
            author = data.xpath('//*[@id="itemContainer"]/div[%d]/a[2]/text()' % i)
            title = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/text()' % i)
            if data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/font/text()' % i) != []:
                isTop = "[置顶]"
            else:
                isTop = ""
            self.__logger.info("获取到%s 《%s》通知，发布时间%s" % (isTop, title[0], time[0]))
            self.__cacheList.append(
                {"title": title[0], "time": time[0], "href": self.__domain + self.__direct + href[0],
                 "author": author[0], 'top': isTop})

        return self.__cacheList

    def getContentCache(self, target):
        rtnContent = []
        for i in target:
            tmpResult = ""
            tmpAttach = {}
            tmpLongTitle = ""
            self.__logger.info("正在获取%s《%s》..." % (i['top'], i['title']))
            '''同时获取完整标题、时间'''
            html = requests.get(i['href'], headers=self.__header)
            html = html.content.decode("utf-8", 'replace')

            data = etree.HTML(html)
            content = data.xpath('/html/body//div')
            for j in content:
                if str(j.get('class')).find("content_time") != -1:
                    time = j.xpath('./text()')[0]
                    self.__logger.info("完整时间：%s" % time)
                    self.__logger.info("链接：%s" % i['href'])
                elif str(j.get('class')).find("content_t") != -1:
                    tmpLongTitle = j.xpath('./text()')[0]
                    self.__logger.notice("获取成功！完整标题：%s" % tmpLongTitle)
                if str(j.get('class')).find("content_font") != -1:
                    """目前发现通知网页有两种方法，一种是经过混淆的，另一种是没有混淆的，先尝试有混淆的"""
                    for k in j.xpath('.//p'):
                        for m in k.xpath('.//text()'):
                            tmpResult = tmpResult + m
                        tmpResult = tmpResult + "\t\n"
                    tmpResult = tmpResult.replace("\xa0", " ")
                    if tmpResult == "":
                        tmpResultList = j.xpath('.//text()')
                        for l in tmpResultList:
                            tmpResult += str(l)
                        tmpResult = tmpResult.replace("\xa0", " ")
                        tmpResult = tmpResult.replace("    ", "\t\n\t")
                if str(j.get('class')).find("news_aboutFile") != -1:
                    # 附件存在
                    # 获取InfomationID
                    sc = str(html)
                    start = sc.find("informationId=")
                    start = sc.find("\'", start)
                    end = sc.find("\'", start + 1)
                    sc = sc[start + 1:end]
                    url = self.__domain + self.__direct + self.__linkBaseUrl
                    for k in j.xpath('.//span'):
                        attSave = str(k.get('id'))
                        attName = str(k.get('title'))
                        send = parse.quote(attSave + "@" + attName + "@" + str(sc))
                        send = "res=" + send
                        rJson = str(requests.post(url, send, headers=self.__header).text)
                        link = self.__domain + self.__direct + self.__downloadBaseUrl + str(rJson)
                        link = link.replace('\r', "")
                        link = link.replace('\n', "")
                        tmpAttach.update({str(k.get('title')): link})

            rtnContent.append(
                {'title': tmpLongTitle, 'address': i['href'], 'time': time, 'author': i['author'],
                 'content': tmpResult, 'attach': tmpAttach, 'sTitle': i['title'], 'top': i['top'],
                 'linkqrcode': "http://qr.topscan.com/api.php?text="+i['href']})
        return rtnContent

    def createContentCache(self):
        self.__cacheContent = self.getContentCache(self.__cacheList)
        self.__cacheContent = self.__cacheSort(self.__cacheContent)

    def get(self):
        return self.__cacheContent

    def createCache(self):
        self.createListCache()
        self.createContentCache()
