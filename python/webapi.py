import sys
import requests
import json
textWrite=True

if sys.argv[1]=="ip":
    if sys.argv=="ip":
        url="https://whois.pconline.com.cn/ip.jsp?ip="+sys.argv[2]
        text=requests.get(url)
        text=text.text
        text=text.replace("\r\n","")
        text=text.replace("\n","")
        text=text.replace(" ","")
####################################################### 
    elif sys.argv[1]=="pos":
        position=sys.argv[2].replace("，",",")
        url="http://api.map.baidu.com/reverse_geocoding/v3/?ak=2qsQNbDMv4WTULwApsVu8IGl7hEr3p3W&output=json&coordtype=wgs84ll&location="+position
        print(url)
        otext=requests.get(url)
        outr=json.loads(otext.text)
        print(outr)
        if not outr["status"]==0:
            text=outr["message"]
        elif outr["result"]["addressComponent"]["country_code"]==-1:
            text="暂不支持查找此地，例子：\n pos 39.983424,116.3229"
        else:
            out=outr["result"]["addressComponent"]
            print(out)
            text="位置： "+out["country"]+"  "+out["province"]+"  "+out["city"]+" "+out["district"]+"\n"+"地址： "+outr["result"]["formatted_address"]
####################################################### 
with open(r"D:\Program Source\QQBOT\python\Temp\temp.txt","w+",encoding="UTF-8") as f:
    if(textWrite):
        text=str(text)
        f.write(text)
        print(text)