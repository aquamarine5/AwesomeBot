import sys
import requests
from json import loads
from googletrans import Translator
from googletrans.constants import (LANGUAGES)
from bs4 import BeautifulSoup
import random
import os
import re
import urllib
import time
import hashlib
arg = sys.argv


class webapi():
    def __init__(self, arg):
        textWrite = True
        text = ""
        imageDict = {
            "": 1,
            "?": 2,
            "宠物": 3,
            "狗": 3,
            "猫": 3,
            "明星": 5
        }
        labelDict = {
            1: "暴恐违禁",
            2: "文本色情",
            3: "政治敏感",
            4: "恶意推广",
            5: "低俗辱骂",
            6: "低俗灌水"
        }
        trsBaiduDict = {
            "韩语": "kor",
            "韩国": "kor",
            "葡萄牙语": "pt",
            "葡萄牙": "pt",
            "希腊语": "el",
            "希腊": "el",
            "保加利亚语": "bul",
            "保加利亚": "bul",
            "文言文": "wyw",
            "粤语": "yue",
            "阿拉伯语": "ara",
            "阿拉伯": "ara",
            "德语": "de",
            "荷兰语": "nl",
            "荷兰": "nl",
            "英语": "en",
            "English": "en",
            "英文": "en",
            "日语": "jp",
            "日本": "jp",
            "俄语": "ru",
            "波兰语": "pl",
            "中文": "zh"
        }
        forBaiduHeader = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://ai.baidu.com/tech/imagerecognition/general",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69",
            "Origin": "https://ai.baidu.com",
            "Cookie": "BAIDUID=1313CB7CF24038805C23D34EDFF25C8A:SL=0:NR=10:FG=1; BIDUPSID=FEC6A91EA1B1B4707809110B7D14EC1C; PSTM=1568465428; BDUSS=R6OG1LZUR4Ri10QzhGNzJVYk1oWFZZU2pjRWIwNHhOSUpPbDUzeEphc29sbVJmRVFBQUFBJCQAAAAAAAAAAAEAAADE8KcAandzaGkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgJPV8oCT1fRF; BDUSS_BFESS=R6OG1LZUR4Ri10QzhGNzJVYk1oWFZZU2pjRWIwNHhOSUpPbDUzeEphc29sbVJmRVFBQUFBJCQAAAAAAAAAAAEAAADE8KcAandzaGkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgJPV8oCT1fRF; H_WISE_SIDS=154770_156537_159234_158935_149355_158405_156816_156289_150776_148867_156096_154605_153628_158926_154173_150772_151018_157261_127969_154413_154175_152982_158528_154013_155803_146732_159014_131423_157699_128701_132550_159288_159450_107313_158055_158830_154189_158519_155344_155255_158022_157171_157790_144966_154619_157814_158718_158610_157188_157965_147551_159050_158367_158910_156710_157696_154639_159157_159092_154362_159074_110085_157006; __yjsv5_shitong=1.0_7_009f894a4cd625acd6f95ba620d853e7fa1f_300_1605529444716_101.20.43.54_9d31cd61; BDRCVFR[mkUqnUt8juD]=mk3SLVN4HKm; H_PS_PSSID=32820_1447_33102_33058_31253_32970_33098_33100_32961_32845; delPer=0; PSINO=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_8b973192450250dd85b9011320b455ba=1605529451,1605617148; BA_HECTOR=0l0la08ga1ah8088sa1fr7hg40p; Hm_lpvt_8b973192450250dd85b9011320b455ba=1605617728"
        }
        headersParameters = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63'}
        if len(arg) == 3:
            if arg[1] == "ip":  # 根据ip看地址
                url = "https://whois.pconline.com.cn/ip.jsp?ip="+arg[2]
                text = requests.get(url)
                text = text.text
                text = text.replace("\r\n", "")
                text = text.replace("\n", "")
                text = text.replace(" ", "")
#######################################################
            elif arg[1] == "pos":  # 根据坐标看地址
                position = arg[2].replace("，", ",")
                url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=2qsQNbDMv4WTULwApsVu8IGl7hEr3p3W&output=json&coordtype=wgs84ll&location="+position
                otext = requests.get(url)
                outr = loads(otext.text)
                if not outr["status"] == 0:
                    text = outr["message"]
                elif outr["result"]["addressComponent"]["country_code"] == -1:
                    text = "暂不支持查找此地，例子：\n pos 39.983424,116.3229"
                else:
                    out = outr["result"]["addressComponent"]
                    text = "位置： "+out["country"]+"  "+out["province"]+"  "+out["city"] + \
                        " "+out["district"]+"\n"+"地址： " + \
                        outr["result"]["formatted_address"]
#######################################################
            elif arg[1] == "photo":  # 每日一图
                url = "http://imagzine.oppomobile.com/api/slide_image/channel_image_list"
                lists = [b"\x08\x01\x10\x01", b"\x08\x02\x10\x01", b"\x08\x03\x10\x01",
                         b"\x08\x04\x10\x01", b"\x08\x05\x10\x01", b"\x08\x06\x10\x01",
                         b"\x08\x07\x10\x01", b"\x08\x08\x10\x01", b"\x08\x09\x10\x01"]
                if arg[2] == "-1":
                    pst = random.choice(lists)
                else:
                    try:
                        if(len(arg[2]) == 1):
                            pst = lists[int(arg[2])]
                        else:
                            if arg[2] in imageDict:
                                pst = lists[imageDict[arg[2]]]
                            else:
                                self.text = "参数不对，目前仅支持 ** 数字 **"
                                self.textWrite = True
                                return
                    except ValueError:
                        self.text = "参数必须是数字"
                        self.textWrite = True
                        return
                    except IndexError:
                        self.text = "数字必须在1-9（包括1,9）以内"
                        self.textWrite = True
                        return
                data = requests.post(url, pst).text
                dt = data.split("android.intent.action.VIEW")
                rd = random.randint(0, len(dt)-1)
                # print(dt[rd])
                dt = dt[rd].split("@")
                if(len(dt) == 2):
                    dt = dt[1][3:].split("Z�")
                else:
                    self.text = "你真倒霉，服务器发来了一些我看不懂的东西"
                    self.textWrite = True
                    return
                text = dt[0].split("R")
                try:
                    text = text[0]+"\n"+text[1][1:]
                except IndexError:
                    self.text = "你真倒霉，服务器发来了一些我看不懂的东西"
                    self.textWrite = True
                    return
                img = ("http"+(dt[1][1:].split("zbhttp")[1])
                       ).split(".jpg")[0]+".jpg"
                ps = "D:\\Program Source\\QQBOT\\python\\Temp\\Photo\\%s.png" % text.replace(
                    "\n", "_").replace("，", ",").replace("。", ".").replace("！", "!").replace("？", "")
                if not (os.path.exists(ps)):
                    image = requests.get(img)
                    with open(ps, "wb+") as f:
                        f.write(image.content)
                text = ps+"|"+text
#######################################################
            elif arg[1] == "search":  # 搜索建议
                urlBd = f"http://suggestion.baidu.com/su?wd={arg[2]}&action=opensearch&ie=UTF-8"
                urlBing = f"http://cn.bing.com/AS/Suggestions?pt=page.home&mkt=zh-cn&ds=mobileweb&qry={arg[2]}&cp=2&cvid=86388E638B3C48DBA852C0BF46189C46"
                urlSg = f"http://www.sogou.com/suggnew/ajajjson?key={arg[2]}&type=web&ori=yes&pr=web"
                url360 = f"http://sug.so.360.cn/suggest?encodein=utf-8&encodeout=utf-8&format=json&word={arg[2]}"
                sgBd = eval(requests.get(urlBd).text)[1]
                sgBing = BeautifulSoup(requests.get(
                    urlBing).text, "html.parser").find_all("span")
                sgSg = eval(requests.get(urlSg).text.replace(
                    "window.sogou.sug", "").replace(";", ""))[0][1]
                sg360 = loads(requests.get(url360).text)["result"]
                text = "这是%s的搜索建议：\n" % arg[2]
                text += "-> 百度：\n"
                for bd in range(len(sgBd)):
                    if bd >= 10:
                        break
                    text += sgBd[bd]
                    if not bd+1 == len(sgBd):
                        text += "，"
                text += "\n-> 必应：\n"
                for bing in range(len(sgBing)):
                    if bing >= 10:
                        break
                    if sgBing[bing].get_text() == "":
                        continue
                    if sgBing[bing].get_text() == "国际版":
                        continue
                    text += sgBing[bing].get_text()
                    if not bing+1 == len(sgBing):
                        text += "，"
                text += "\n-> 搜狗：\n"
                for sogou in range(len(sgSg)):
                    if sogou >= 10:
                        break
                    text += sgSg[sogou]
                    if not sogou+1 == len(sgSg):
                        text += "，"
                text += "\n-> 360搜索：\n"
                for s360 in range(len(sg360)):
                    if s360 >= 10:
                        break
                    text += sg360[s360]["word"]
                    if not s360+1 == len(sg360):
                        text += "，"
#######################################################
            elif arg[1] == "baidu":  # 百度智能搜索
                soup = BeautifulSoup(
                    requests.get(f"http://www.baidu.com/s?wd={urllib.parse.quote(arg[2])}&ie=utf-8", headers=headersParameters).text, 
                    features="html.parser")
                soup = soup.findAll(
                    "div", attrs={"class": "op_exactqa_s_answer"})
                if len(soup) == 0:
                    text = "没有找到结果，功能优化中"
                else:
                    try:
                        text = soup[0].a.text.replace(" ", "").replace("\n", "")
                    except:
                        text = soup[0].text.replace(" ", "").replace("\n", "")
#######################################################
            elif arg[1] == "news":  # 新闻相关搜索
                with open(r"D:\Program Source\QQBOT\python\Source\baiduapi.txt") as f:
                    app = eval(f.read())[5]
                urlNews = "http://index.baidu.com/Interface/Newwordgraph/getNews?"\
                    "region=0&startdate=20200101&enddate=%s&wordlist[0]=%s" % (
                        time.strftime("%Y%m%d", time.localtime()), arg[2])
                cookir = {"BDUSS": app}
                o = loads(requests.get(urlNews, cookies=cookir).text)
                o = o["data"][0]["news"]
                text = f"这是{arg[2]}的今年新闻：\n"
                if len(o) == 0:
                    text += "\n无相关新闻"
                for i in range(len(o)):
                    text = text + \
                        o[i]["source"].split(
                            " ")[1]+" "+o[i]["title"].replace("<em>", "").replace("</em>", "")
                    if not i+1 == len(o):
                        text += "\n"
#######################################################
            elif arg[1] == "face":  # B站随机头像
                textWrite = False
                if (arg[2] == "bilibili") | (arg[2] == "b"):
                    while True:
                        out = self.face()
                        if out == None:
                            pass
                        else:
                            break
                    # print("D:\\0.png")
                    print(out)
                elif (arg[2] == "qq") | (arg[2] == "q"):
                    while True:
                        out = self.faceqq()
                        if out == 1:
                            pass
                        else:
                            break
            elif arg[1] == "imageSearch":
                url = "https://ai.baidu.com/aidemo"
                info = loads(requests.post(
                    url, data=f"image&image_url={arg[2]}&type=advanced_general&baike_num=1", headers=forBaiduHeader).text)

#######################################################
        elif len(arg) == 4:
            if arg[1] == "trsWd":
                if (arg[3] == "YouDao") | (arg[3] == "-"):  # 翻译单词
                    if " " in arg[2]:
                        self.text = "请删除单词内空格"
                        self.textWrite = True
                        return
                    urlTs = f"http://dict.iciba.com/dictionary/word/suggestion?client=6&is_need_mean=1&nums=10&word={arg[2]}"
                    Ts = loads(requests.get(urlTs).text)
                    text = f"这是{arg[2]}的相近词解释：\n"
                    for i in Ts["message"]:
                        text += f"{i['key']} ：{i['paraphrase']}\n"
#######################################################
            elif arg[1] == "zyb":  # 作业帮
                urlBd = f"http://www.baidu.com/s?ie=UTF-8&wd=site:www.zybang.com%20{arg[2]}"
                o = BeautifulSoup(requests.get(
                    urlBd, headers=headersParameters).text, features="html.parser")
                link = o.findAll("h3", attrs={"class", "t"})[
                    int(arg[3])].a["href"]
                zyb = BeautifulSoup(
                    re.sub("<br>|<br/>", "", requests.get(link).text), features="html.parser")
                t = zyb.findAll(
                    "dl", attrs={"class": "card qb_wgt-question nobefore"})[0].dd.span
                answer = zyb.findAll(
                    "dl", attrs={"id": "good-answer"})[0].dd.span
                tbs = t.findAll("img")
                title = re.sub(r"<img(.*?)>|<img(.*?)/>", "{img}", str(t))
                title = re.sub(r"<br>|</br>", "\n", title)
                title = re.sub(r'<(.*?)>', "", title)
                ab = answer.findAll("img")
                answer = re.sub(r"<img(.*?)>|<img(.*?)/>", "{img}", str(answer))
                answer = re.sub(r"<br>|</br>", "\n", answer)
                answer = re.sub(r'<(.*?)>', "", answer)
                count = 0
                for i in range(len(tbs)):
                    with open(f"D:\\Program Source\\QQBOT\\python\\Temp\\Study\\{count}.jpg", "wb+") as f:
                        f.write(requests.get(tbs[i]["src"]).content)
                    count += 1
                for j in range(len(ab)):
                    with open(f"D:\\Program Source\\QQBOT\\python\\Temp\\Study\\{count}.jpg", "wb+") as f:
                        f.write(requests.get(ab[j]["src"]).content)
                    count += 1
                text = title+"的答案是：\n"+answer
                text = re.sub("&nbsp;", "", text)
                text = re.sub("&amp;", "&", text)
                text = re.sub("&gt;", ">", text)
#######################################################
        elif len(arg) == 2:
            if arg[1] == "math":  # 数学题
                textWrite = False
                url = "http://e.anoah.com/api/?q=json/ebag/ValidateCode/getImageCode&info={\"uid\":\"114514\"}"
                with open(r"D:\Program Source\QQBOT\python\Temp\Math.png", "wb+") as f:
                    f.write(requests.get(url).content)
#######################################################
            elif arg[1] == "hot":  # 微博热搜
                url = "http://api.weibo.cn/2/guest/page?"\
                    "from=1781065010&c=wbfastapp&lang=zh_CN&count=20&containerid=106003type%3D25%26t%3D3%26"\
                    "disable_hot%3D1%26filter_type%3Drealtimehot&lfid=OPPO_qjs"
                o = loads(requests.get(url).text)
                o = o["cards"][0]["card_group"]
                text = "微博热搜：\n"
                for i in range(len(o)):
                    text += str(i+1)+" "+o[i]["desc"]+"\n"
#######################################################
            elif arg[1] == "hotword":  # B站热词
                url = "http://s.search.bilibili.com/main/hotword"
                o = loads(requests.get(url).text)["list"]
                text = "B站热词：\n"
                for i in range(len(o)):
                    text = text+o[i]["keyword"]+"，"
        if(len(arg) != 1):
            ######################################################
            if arg[1] == "check":
                s = ''.join(arg[2:])
                textWrite = False
                url = "https://ai.baidu.com/aidemo"
                head = forBaiduHeader
                head["Referer"] = "https://ai.baidu.com/tech/textcensoring"
                tex = f"content={urllib.parse.quote(s)}&type=textcensor&apiType=censor&requestTime=1606136419887&token=3466a61eb8"
                t = requests.post(url, tex, headers=head).text
                t = t.encode("utf-8").decode("unicode_escape")
                l = loads(t)["data"]["result"]["reject"]
                if(len(l) == 0):
                    text = "通过"
                else:
                    text = labelDict[l[0]["label"]]+f"\n{str(l)}"
                with open(r"D:/Program Source/QQBOT/python/Temp/check.txt", "w+", encoding="UTF-8") as f:
                    f.write(text)
            if arg[1] == "trs":
                if (arg[2] == "粤语") | (arg[2] == "文言文") | (arg[2] == "文言文中文") | (arg[2] == "粤语中文") | (arg[3] == "b"):  # 翻译（百度）
                    app = []
                    with open(r"D:\Program Source\QQBOT\python\Source\baiduapi.txt") as f:
                        app = eval(f.read())
                    appid = app[3]
                    secretKey = app[4]
                    fromLang = 'auto'
                    info = " ".join(arg[4:])
                    if(arg[2] == "文言文中文"):
                        fromLang = "wyw"
                        toLang = "zh"
                    elif (arg[2] == "粤语中文"):
                        fromLang = "yue"
                        toLang = "zh"
                    else:
                        if (arg[2] not in trsBaiduDict):
                            self.text = "错误的语言，尝试 help 百度翻译"
                            self.textWrite = True
                            return
                    toLang = trsBaiduDict[arg[2]]
                    salt = random.randint(32768, 65536)
                    sign = appid + str(info) + str(salt) + secretKey
                    sign = hashlib.md5(sign.encode()).hexdigest()
                    # q=urllib.parse.quote(arg[3:])
                    myurl = f"http://api.fanyi.baidu.com/api/trans/vip/translate?appid={appid}&q={urllib.parse.quote(info)}&from={fromLang}&to={toLang}&salt={salt}&sign={sign}"
                    text = loads(requests.get(myurl).text.encode(
                        "utf-8").decode("unicode_escape"))["trans_result"][0]["dst"]
    #######################################################
                elif(arg[3] == "Google") | (arg[3] == "g") | (arg[3] == "1"):  # 翻译（谷歌）
                    if arg[2] == "中文":
                        dest = "zh-cn"
                    elif arg[2] == "简体中文":
                        dest = "zh-cn"
                    elif arg[2] == "繁体中文":
                        dest = "zh-tw"
                    elif arg[2] == "日语":
                        dest = "ja"
                    elif (arg[2] == "英语") | (arg[2] == "英文"):
                        dest = "en"
                    elif arg[2] == "德语":
                        dest = "de"
                    elif arg[2] == "加泰罗尼亚语":
                        dest = "ca"
                    elif arg[2] == "塔吉克语":
                        dest = "tg"
                    elif arg[2] == "孟加拉语":
                        dest = "bn"
                    elif arg[2] == "法语":
                        dest = "fr"
                    elif (arg[2] == "犹太语") | (arg[2] == "依地语"):
                        dest = "yi"
                    elif arg[2] == "芬兰语":
                        dest = "fi"
                    elif arg[2] == "葡萄牙语":
                        dest = "pt"
                    elif (arg[2] == "保加利亚") | (arg[2] == "保加利亚语"):
                        dest = "bg"
                    elif arg[2] == "祖鲁语":
                        dest = "zu"
                    elif (arg[2] == "朝鲜语") | (arg[2] == "韩国语") | (arg[2] == "韩语"):
                        dest = "ko"
                    elif arg[2] == "库尔德语":
                        dest = "ku"
                    elif arg[2] == "南非语":
                        dest = "af"
                    elif arg[2] == "希腊语":
                        dest = "el"
                    elif arg[2] == "西班牙语":
                        dest = "es"
                    elif (arg[2] == "象形") | (arg[2] == "阿姆哈拉文"):
                        dest = "am"
                    elif (arg[2] == "阿拉伯语") | (arg[2] == "阿拉伯"):
                        dest = "ar"
                    else:
                        if arg[2] not in LANGUAGES:
                            self.text = "错误的语言，如需翻译文言文等中文变体请使用：\n 翻译 [需要翻译文本] 文言文\n文言文转中文请使用：翻译 [需要翻译文本] 文言文中文"\
                                "\n空格请用+代替谢谢"
                            self.textWrite = True
                            return
                        else:
                            dest = arg[3]
                    trsor = Translator(service_urls=["translate.google.cn"])
                    inp = " ".join(arg[4:])
                    try:
                        text = trsor.translate(inp, dest=dest).text
                    except AttributeError:
                        text = "谷歌翻译服务器的土豆可能发芽了"
            elif arg[1] == "trsmt":
                pass  # 翻译20次生草机
#######################################################
        self.text = text
        self.textWrite = textWrite
#######################################################

    def face(self) -> int:
        r = random.randint(1, 666666666)
        url = f"http://api.bilibili.com/x/space/acc/info?mid={r}"
        o = loads(requests.get(url).text)
        if o["code"] == (-404):
            return None
        elif o["data"]["face"] == "http://i0.hdslb.com/bfs/face/member/noface.jpg":
            return None
        else:
            with open(f"D:\\Program Source\\QQBOT\\python\\Temp\\Face\\{r}.jpg", "wb+") as f:
                f.write(requests.get(o["data"]["face"]).content)
            return r

    def faceqq(self):
        return 0
#######################################################


if __name__ == "__main__":
    wb = webapi(arg)
    try:
        # wb=webapi(arg)
        text = wb.text
        textWrite = wb.textWrite
    except BaseException as e:
        text = e
        textWrite = True
    if(False):
        with open(r"D:\Program Source\QQBOT\python\Temp\temp.txt", "w+", encoding="UTF-8") as f:
            if(textWrite):
                text = str(text)
                f.write(text)
                print(text)
    else:
        print(text)
