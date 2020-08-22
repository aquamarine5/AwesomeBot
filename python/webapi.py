import sys
import requests
from json import loads
from googletrans import Translator
from googletrans.constants import (LANGUAGES)
from bs4 import BeautifulSoup
import random
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
                if(arg[4]=="Google")|(arg[4]=="-"):
                    if   arg[3]=="中文":dest="zh-cn"
                    elif arg[3]=="简体中文":dest="zh-cn"
                    elif arg[3]=="繁体中文":dest="zh-tw"
                    elif arg[3]=="日语":dest="ja"
                    elif arg[3]=="英语":dest="en"
                    elif arg[3]=="德语":dest="de"
                    elif arg[3]=="加泰罗尼亚语":dest="ca"
                    elif arg[3]=="孟加拉语":dest="bn"
                    elif arg[3]=="法语":dest="fr"
                    elif arg[3]=="祖鲁语":dest="zu"
                    elif (arg[3]=="朝鲜语")|(arg[3]=="韩国语")|(arg[3]=="韩语"):dest="ko"
                    elif arg[3]=="库尔德语":dest="ku"
                    elif arg[3]=="南非语":dest="af"
                    elif (arg[3]=="象形")|(arg[3]=="阿姆哈拉文"):dest="am"
                    elif (arg[3]=="阿拉伯语")|(arg[3]=="阿拉伯"):dest="ar"
                    else:
                        if arg[3] not in LANGUAGES:
                            self.text="错误的语言"
                            self.textWrite=True
                            return
                        else:
                            dest=arg[3]
                    trsor=Translator(service_urls=["translate.google.cn"])
                    inp=arg[2].replace("+"," ")
                    text=trsor.translate(inp,dest=dest).text
                elif arg[4]=="Baidu":
                    #/urlts="http://api.fanyi.baidu.com"
                    appid = '20200820000547489'  # 填写你的appid
                    secretKey = 'c8tMufVsKLEPRmdhxCKJ'  # 填写你的密钥
                    fromLang = 'auto'   #原文语种
                    toLang = 'zh'   #译文语种
                    salt = random.randint(32768, 65536)
                    q= 'apple'
                    sign = appid + q + str(salt) + secretKey
                    sign = hashlib.md5(sign.encode()).hexdigest()
                    myurl = myurl + '?appid=20200820000547489&q=%s&from=%s&to=%s&salt=%s&sign=%s'%(q,fromLang,toLang,salt,sign)
        elif len(arg)==2:
            if arg[1]=="math":
                textWrite=False
                url="http://e.anoah.com/api/?q=json/ebag/ValidateCode/getImageCode&info={\"uid\":\"114514\"}"
                with open(r"D:\Program Source\QQBOT\python\Temp\Math.png","wb+") as f:f.write(requests.get(url).content)
            elif arg[1]=="photo":
                url="http://imagzine.oppomobile.com/api/slide_image/channel_image_list"
                data=requests.post(url,b"\x08\x01\x10\x01").text
                dt=data.split("android.intent.action.VIEW")
                rd=random.randint(0,len(dt)-1)
                dt=dt[rd].split("\x10@\x01J")[1][1:].split("Z�\x02")
                text=dt[0]
                img=("http"+(dt[1].split("zbhttp")[1])).split(".webp")[0]+".webp"
                image=requests.get(img)
                with open(r"D:\Program Source\QQBOT\python\Temp\photo.png","wb+") as f:f.write(image.content)
        self.text=text
        self.textWrite=textWrite
####################################################### 

if __name__=="__main__":
    try:
        wb=webapi(arg)
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
