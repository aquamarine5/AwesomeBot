import requests
import sys
import json

textWrite=True

def yxpTimeGet():
    url="http://e.anoah.com/api_dist/?q=json/ebag/System/getServerTime&info={}"
    out=requests.get(url)
    out=json.loads(out.text)
    return out["recordset"]["system_time"]
def yxpName(uid):
    url="https://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s"%(uid,str(yxpTimeGet()))
    return json.loads(requests.get(url).text)["recordset"]["real_name"]
def yxpClassId(uid):
    return 0
####################################################### 
if len(sys.argv)==3:
    if sys.argv[1]=="ip":
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
    elif sys.argv[1]=="yxpDCom":
        url="http://e.anoah.com/api_cache/?q=json/icom/Dcom/getDCom&info={\"dcom_id\":%s}"%int(sys.argv[2])
        print(url)
        out=requests.get(url)
        out=json.loads(out.text)
        if "status" in out:
            text="指定的作业不存在"
        else:
            text="""优学派作业ID：%s    
创建时间：%s    
作业名称：%s    
作业标题：%s    
活动名称：%s    
描述：%s"""%(str(out["id"]),str(out["create_time"]),str(out["dcom_name"]),str(out["dcom_title"]),str(out["activity_name"]),str(out["description"]))
####################################################### 
    elif sys.argv[1]=="yxpPic":
        url="https://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s"%(sys.argv[2],str(yxpTimeGet()))
        out=requests.get(url)
        out=json.loads(out.text)
        urlPic="http://static.anoah.com"
        urlJson=out["recordset"]["avatar"]
        urlJson=urlJson.replace(r"\/","/")
        if(urlJson.startswith("http")):
            urlPic=urlJson
            urlPic2="http://www.anoah.com/ebag/static/images/noavatar.jpg"
        else:
            urlPic=urlPic+urlJson
            urlPic2=urlPic.replace(".jpg","_private.jpg")
        Pic=requests.get(urlPic)
        with open(r"D:\Program Source\QQBOT\python\Temp\FacePublic.jpg","wb+") as f:
            f.write(Pic.content)
        Pic2=requests.get(urlPic2)
        with open(r"D:\Program Source\QQBOT\python\Temp\FacePrivate.jpg","wb+") as f:
            f.write(Pic2.content)
        text=yxpName(sys.argv[2])
#######################################################
    elif sys.argv[1]=="yxpInfo":
        time=yxpTimeGet()
        urlHaoTiBen="https://e.anoah.com/api/?q=json/ebag5/Qtibook/readBookStatus&info={\"start_time\":\"2008-08-08+00:00:00\",\"user_id\":%s}&pmatsemit=%s"%(sys.argv[2],time)
        urlClass="https://e.anoah.com/api/?q=json/ebag5/User/getUserClasses&info={\"userid\":%s}&pmatsemit=%s"%(sys.argv[2],time)
        urlScore="https://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s"%(sys.argv[2],time)
        urlScore2="https://e.anoah.com/api/?q=json/ebag/user/score/score_count&info={\"userid\":%s}"%sys.argv[2]
        urlScore3="https://e.anoah.com/api/?q=json/ebag/user/score/score_detail&info={\"userid\":%s,\"pagesize\":10,\"page\":1,\"start\":\"\",\"end\":\"\"}&pmatsemit=%s"%(sys.argv[2],time)
        HaoTi=json.loads(requests.get(urlHaoTiBen).text)
        Class=json.loads(requests.get(urlClass).text)
        ClassScore=""
        for t in range(0,len(Class["recordset"])):
            if t==0:
                ClassScore=Class["recordset"][t]["class_id"]
            else:
                ClassScore=str(ClassScore)+","+str(Class["recordset"][t]["class_id"])
        urlClassIn="https://api2.anoah.com/jwt/user/classes/subjects?class_id=%s&pmatsemit=%s"%(ClassScore,time)
        urlHomework="https://e.anoah.com/api/?q=json/ebag5/Homework/readHomeworkStat&info={\"to\":\"\",\"class_ids\":\"%s\",\"user_id\":%s,\"from\":\"\"}&pmatsemit=%s"%(ClassScore,sys.argv[2],time)
        Score=json.loads(requests.get(urlScore).text)
        Score2=json.loads(requests.get(urlScore2).text)
        Score3=json.loads(requests.get(urlScore3).text)
        ClassIn=json.loads(requests.get(urlClassIn).text)
        Homework=json.loads(requests.get(urlHomework).text)
        #---------------------------------------------
####################################################### 
elif len(sys.argv)==2:
    if sys.argv[1]=="yxpTIME": 
        text=yxpTimeGet()
    elif sys.argv=="yxpJWT":
        urln="https://emessage.anoah.com/api/?q=json/jwt/Emessage/get_list_latest&info={\"message_types\":\"0,1,2\",\"user_id\":1585732}&pmatsemit="+str(yxpTimeGet())
        outn=requests.get(urln)
        text=outn.text
    else:
        text="Error"
#######################################################
elif len(sys.argv)==4:
    if sys.argv[1]=="yxpHw":
        time=yxpTimeGet()
        urlClass="https://e.anoah.com/api/?q=json/ebag5/User/getUserClasses&info={\"userid\":%s}&pmatsemit=%s"%(sys.argv[2],time)
        Class=json.loads(requests.get(urlClass).text)
        ClassScore=""
        for t in range(0,len(Class["recordset"])):
            if t==0:
                ClassScore=Class["recordset"][t]["class_id"]
            else:
                ClassScore=str(ClassScore)+","+str(Class["recordset"][t]["class_id"])
        #---------------------------------------------
        if  (sys.argv[3]=="语文"):classId=1
        elif(sys.argv[3]=="数学"):classId=2
        elif(sys.argv[3]=="英语"):classId=3
        elif(sys.argv[3]=="历史"):classId=5
        elif(sys.argv[3]=="地理"):classId=6
        elif(sys.argv[3]=="生物"):classId=7
        elif(sys.argv[3]=="物理"):classId=8
        elif(sys.argv[3]=="美术"):classId=32
        elif(sys.argv[3]=="信息"):classId=33
        elif(sys.argv[3]=="音乐"):classId=14
        elif(sys.argv[3]=="体育"):classId=23
        elif(sys.argv[3]=="道法"):classId=437
        #---------------------------------------------
        urlNOK="http://api2.anoah.com/jwt/homework/publish/getListForStudent?user_id=%s&status=0&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=20&pmatsemit=%s"%(sys.argv[2],str(classId),ClassScore,time)
        urlOk="http://api2.anoah.com/jwt/homework/publish/getListForStudent?user_id=%s&status=1&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=20&pmatsemit=%s"%(sys.argv[2],str(classId),ClassScore,time)
        ok=json.loads(requests.get(urlOk).text.encode('utf-8').decode("unicode_escape"))
        nok=json.loads(requests.get(urlNOK).text.encode('utf-8').decode("unicode_escape"))
        if(ok["status"]==0):
            text=ok["msg"]
        else:
        #---------------------------------------------
            okjs=ok["recordset"]
            nokjs=nok["recordset"]
            text="这是"+yxpName(sys.argv[2])+"的"+sys.argv[3]+"作业情况：\n"
            lists=okjs["lists"]
            noklists=nokjs["lists"]
            write=1
            if(okjs["total_count"]==0):
                text="没有写了的作业。\n"
                write=0
            else:
                for i in range(0,int(okjs["total_count"])):
                    if i==0:
                        text=text+"☛ 写了的作业（%s个）：\n"%(okjs["total_count"])
                    text=text+lists[i]["start_time"]+" "+lists[i]["title"]+" "+lists[i]["subject_name"]+lists[i]["teacher_name"]#+"\n作业ID："+lists[i]["course_hour_publish_id"]
                    if not i==int(okjs["total_count"]):
                        text=text+"\n"
                if (int(okjs["per_page"])<int(okjs["total_count"])):
                    text=text+"※ 仅显示%s个，但一共有%s个作业完成\n"%(int(okjs["per_page"]),int(okjs["total_count"]))
            if(nokjs["total_count"]==0):
                if(write==0):
                    text="老师没留过作业。"
                else:
                    text=text+"没有没写的作业。"
            else:
                for i in range(0,int(nokjs["total_count"])):
                    if i==0:
                        text=text+"☛ 没写的作业（%s个）：\n"%(nokjs["total_count"])
                    text=text+noklists[i]["start_time"]+" "+noklists[i]["title"]+" "+noklists[i]["subject_name"]+noklists[i]["teacher_name"]#+"\n作业ID："+noklists[i]["course_hour_publish_id"]
                    if not i==int(okjs["total_count"]):
                        text=text+"\n"
                if (int(nokjs["per_page"])<int(nokjs["total_count"])):
                    text=text+"※ 仅显示%s个，但一共有%s个作业未完成"%(int(nokjs["per_page"]),int(nokjs["total_count"]))
#######################################################
    else:
        text="Error"
#######################################################
else:
    text="参数不够"
####################################################### 
with open(r"D:\Program Source\QQBOT\python\Temp\temp.txt","w+",encoding="UTF-8") as f:
    if(textWrite):
        text=str(text)
        f.write(text)
        print(text)