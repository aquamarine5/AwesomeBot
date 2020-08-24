import sys
import requests
from json import loads
from googletrans import Translator
from googletrans.constants import (LANGUAGES)
from bs4 import BeautifulSoup
import random
import os
import urllib
import hashlib
arg=sys.argv
class webapi():
    def __init__(self,arg):
        textWrite=True
        text=""
        if len(arg)==3:
            if arg[1]=="ip":
                url="https://whois.pconline.com.cn/ip.jsp?ip="+arg[2]
                text=requests.get(url)
                text=text.text
                text=text.replace("\r\n","")
                text=text.replace("\n","")
                text=text.replace(" ","")
####################################################### 
            elif arg[1]=="pos":
                position=arg[2].replace("，",",")
                url="http://api.map.baidu.com/reverse_geocoding/v3/?ak=2qsQNbDMv4WTULwApsVu8IGl7hEr3p3W&output=json&coordtype=wgs84ll&location="+position
                otext=requests.get(url)
                outr=loads(otext.text)
                if not outr["status"]==0:
                    text=outr["message"]
                elif outr["result"]["addressComponent"]["country_code"]==-1:
                    text="暂不支持查找此地，例子：\n pos 39.983424,116.3229"
                else:
                    out=outr["result"]["addressComponent"]
                    text="位置： "+out["country"]+"  "+out["province"]+"  "+out["city"]+" "+out["district"]+"\n"+"地址： "+outr["result"]["formatted_address"]
            elif arg[1]=="search":
                urlBd="http://suggestion.baidu.com/su?wd=%s&action=opensearch&ie=UTF-8"%arg[2]
                print(urlBd)
                urlBing="http://cn.bing.com/AS/Suggestions?pt=page.home&mkt=zh-cn&ds=mobileweb&qry=%s&cp=2&cvid=86388E638B3C48DBA852C0BF46189C46"%arg[2]
                urlSg="http://www.sogou.com/suggnew/ajajjson?key=%s&type=web&ori=yes&pr=web"%arg[2]
                url360="http://sug.so.360.cn/suggest?encodein=utf-8&encodeout=utf-8&format=json&word=%s"%arg[2]
                sgBd=eval(requests.get(urlBd).text)[1]
                sgBing=BeautifulSoup(requests.get(urlBing).text,"html.parser").find_all("span")
                sgSg=eval(requests.get(urlSg).text.replace("window.sogou.sug","").replace(";",""))[0][1]
                sg360=loads(requests.get(url360).text)["result"]
                text="这是%s的搜索建议：\n"%arg[2]
                text+="-> 百度：\n"
                for bd in range(len(sgBd)):
                    text+=sgBd[bd]
                    if not bd+1==len(sgBd):text+="，"
                text+="\n-> 必应：\n"
                for bing in range(len(sgBing)):
                    if sgBing[bing].get_text()=="":continue
                    if sgBing[bing].get_text()=="国际版":continue
                    text+=sgBing[bing].get_text()
                    if not bing+1==len(sgBing):text+="，"
                text+="\n-> 搜狗：\n"
                for sogou in range(len(sgSg)):
                    text+=sgSg[sogou]
                    if not sogou+1==len(sgSg):text+="，"
                text+="\n-> 360搜索：\n"
                for s360 in range(len(sg360)):
                    text+=sg360[s360]["word"]
                    if not s360+1==len(sg360):text+="，"
        elif len(arg)==4:
            if arg[1]=="trsWd":
                if (arg[3]=="YouDao")|(arg[3]=="-"):
                    if " " in arg[2]:
                        self.text="请删除单词内空格"
                        self.textWrite=True
                        return
                    urlTs="http://dict.iciba.com/dictionary/word/suggestion?"\
                        "client=6&is_need_mean=1&nums=10&word=%s"%(arg[2])
                    Ts=loads(requests.get(urlTs).text)
                    text="这是%s的相近词解释：\n"%arg[2]
                    for i in Ts["message"]:text+="%s ：%s\n"%(i["key"],i["paraphrase"])
        elif len(arg)==5:
            if arg[1]=="trs":
                if (arg[4]=="Baidu")|(arg[3]=="文言文")|(arg[3]=="文言文中文")|(arg[3]=="0"):
                    app=[]
                    with open(r"python\Source\baiduapi.txt") as f:app=eval(f.read())
                    appid = app[3]
                    secretKey = app[4]
                    fromLang = 'auto'
                    if arg[3]=="中文":toLang="zh"
                    elif arg[3]=="文言文中文":
                        toLang="zh"
                        fromLang="wyw"
                    elif arg[3]=="文言文":toLang="wyw"
                    elif arg[3]=="粤语":toLang="yue"
                    elif arg[3]=="繁体":toLang="cht"
                    elif arg[3]=="繁体中文":toLang="cht"
                    elif arg[3]=="韩语":toLang="kor"
                    elif arg[3]=="泰语":toLang="th"
                    elif arg[3]=="阿拉伯语":toLang="ara"
                    elif arg[3]=="荷兰语":toLang="nl"
                    elif arg[3]=="英文":toLang="en"
                    elif arg[3]=="英语":toLang="en"
                    else:
                        self.text="错误的语言\n如需翻译少数语言请使用：翻译 [需要翻译文本] 祖鲁语"
                        self.textWrite=True
                        return
                    
                    salt = random.randint(32768, 65536)
                    sign = appid + str(arg[2]) + str(salt) + secretKey
                    sign = hashlib.md5(sign.encode()).hexdigest()
                    myurl = "http://api.fanyi.baidu.com/api/trans/vip/translate?appid=%s&q=%s&from=%s&to=%s&salt=%s&sign=%s"%\
                        (appid,urllib.parse.quote(arg[2]),fromLang,toLang,salt,sign)
                    text=loads(requests.get(myurl).text.encode("utf-8").decode("unicode_escape"))["trans_result"][0]["dst"]
                elif(arg[4]=="Google")|(arg[4]=="-")|(arg[4]=="1"):
                    if   arg[3]=="中文":dest="zh-cn"
                    elif arg[3]=="简体中文":dest="zh-cn"
                    elif arg[3]=="繁体中文":dest="zh-tw"
                    elif arg[3]=="日语":dest="ja"
                    elif (arg[3]=="英语")|(arg[3]=="英文"):dest="en"
                    elif arg[3]=="德语":dest="de"
                    elif arg[3]=="加泰罗尼亚语":dest="ca"
                    elif arg[3]=="塔吉克语":dest="tg"
                    elif arg[3]=="孟加拉语":dest="bn"
                    elif arg[3]=="法语":dest="fr"
                    elif (arg[3]=="犹太语")|(arg[3]=="依地语"):dest="yi"
                    elif arg[3]=="芬兰语":dest="fi"
                    elif arg[3]=="葡萄牙语":dest="pt"
                    elif (arg[3]=="保加利亚")|(arg[3]=="保加利亚语"):dest="bg"
                    elif arg[3]=="祖鲁语":dest="zu"
                    elif (arg[3]=="朝鲜语")|(arg[3]=="韩国语")|(arg[3]=="韩语"):dest="ko"
                    elif arg[3]=="库尔德语":dest="ku"
                    elif arg[3]=="南非语":dest="af"
                    elif arg[3]=="希腊语":dest="el"
                    elif arg[3]=="西班牙语":dest="es"
                    elif (arg[3]=="象形")|(arg[3]=="阿姆哈拉文"):dest="am"
                    elif (arg[3]=="阿拉伯语")|(arg[3]=="阿拉伯"):dest="ar"
                    else:
                        if arg[3] not in LANGUAGES:
                            self.text="错误的语言，如需翻译文言文等中文变体请使用：\n 翻译 [需要翻译文本] 文言文\n文言文转中文请使用：翻译 [需要翻译文本] 文言文中文"\
                                "\n空格请用+代替谢谢"
                            self.textWrite=True
                            return
                        else:
                            dest=arg[3]
                    trsor=Translator(service_urls=["translate.google.cn"])
                    inp=arg[2].replace("+"," ")
                    text=trsor.translate(inp,dest=dest).text
                
        elif len(arg)==2:
            if arg[1]=="math":
                textWrite=False
                url="http://e.anoah.com/api/?q=json/ebag/ValidateCode/getImageCode&info={\"uid\":\"114514\"}"
                with open(r"D:\Program Source\QQBOT\python\Temp\Math.png","wb+") as f:f.write(requests.get(url).content)
            elif arg[1]=="photo":
                url="http://imagzine.oppomobile.com/api/slide_image/channel_image_list"
                pst=random.choice(
                    [b"\x08\x01\x10\x01",b"\x08\x03\x10\x01",b"\x08\x08\x10\x01",
                     b"\x08\x09\x10\x01",b"\x08\x02\x10\x01",b"\x08\x07\x10\x01",
                     b"\x08\x06\x10\x01"])
                print(pst)
                data=requests.post(url,pst,timeout=(0.5,0.5)).text
                dt=data.split("android.intent.action.VIEW")
                rd=random.randint(0,len(dt)-1)
                print(rd)
                dt=dt[rd].split("\x10@")[1][3:].split("Z�")
                text=dt[0].split("R")
                text=text[0]+"\n"+text[1][1:]
                img=("http"+(dt[1][1:].split("zbhttp")[1])).split(".jpg")[0]+".jpg"
                ps="D:\\Program Source\\QQBOT\\python\\Temp\\Photo\\%s.png"%text.replace("\n","").replace("，","").replace("。","").replace("！","")
                if not (os.path.exists(ps)):
                    image=requests.get(img)
                    with open(ps,"wb+") as f:
                        f.write(image.content)
                text=ps+"|"+text
            elif arg[1]=="hot":
                url="http://api.weibo.cn/2/guest/page?"\
                    "from=1781065010&c=wbfastapp&lang=zh_CN&count=20&containerid=106003type%3D25%26t%3D3%26"\
                    "disable_hot%3D1%26filter_type%3Drealtimehot&lfid=OPPO_qjs"
                o=loads(requests.get(url).text)
                o=o["cards"][0]["card_group"]
                text="微博热搜：\n"
                for i in range(len(o)):
                    text+=str(i+1)+" "+o[i]["desc"]+"\n"
        self.text=text
        self.textWrite=textWrite
####################################################### 

if __name__=="__main__":
    wb=webapi(arg)
    try:
        
        text=wb.text
        textWrite=wb.textWrite
    except BaseException as e:
        text=e
        textWrite=True
    with open(r"D:\Program Source\QQBOT\python\Temp\temp.txt","w+",encoding="UTF-8") as f:
        if(textWrite):
            text=str(text)
            f.write(text)
            print(text)
