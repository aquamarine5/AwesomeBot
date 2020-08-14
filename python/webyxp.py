import requests
import sys
import json

is_pydroid=False
if(is_pydroid):
    arg="python yxpRs 1585738 最新".split(" ")
else:
    arg=sys.argv
def yxpTimeGet():
    urlT="http://e.anoah.com/api_dist/?q=json/ebag/System/getServerTime&info={}"
    return json.loads(requests.get(urlT).text)["recordset"]["system_time"]
def yxpName(uid):
    urlN="http://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s"%(uid,str(yxpTimeGet()))
    return json.loads(requests.get(urlN).text)["recordset"]["real_name"]
def yxpClassId(uid):
    urlClass="http://e.anoah.com/api/?q=json/ebag5/User/getUserClasses&info={\"userid\":%s}&pmatsemit=%s"%(uid,yxpTimeGet())
    Class=json.loads(requests.get(urlClass).text)["recordset"]
    ClassScore=""
    for t in range(0,len(Class)):
        if t==0:
            ClassScore=Class[t]["class_id"]
        else:
            ClassScore=str(ClassScore)+","+str(Class[t]["class_id"])
    return ClassScore
def yxpToText(inp):
    inp=inp.replace("<p>","")
    inp=inp.replace(r"</p>","")
    inp=inp.replace("<span class=\"spot\">","")
    inp=inp.replace("<span style=\"font-weight:bold\">","")
    inp=inp.replace("<span style=\"color:blue\">","")
    inp=inp.replace(r"</span>","")
    inp=inp.replace("&nbsp;","")
    inp=inp.replace("<pos>","")
    inp=inp.replace(r"</pos>","")
    inp=inp.replace(r"<br  />","")
    inp=inp.replace(r"<br />","")
    inp=inp.replace('<p align=\"center\">',"")
    inp=inp.replace("<img","`")
    inp=inp.replace(">","~")
    s=inp.find("`")
    e=inp.find("~")
    if s==-1:inp=inp[:s]+inp[e+1:]
    return inp
####################################################### 
subjectList={"语文":1,"数学":2,"英语":3,"化学":4,"历史":5,"地理":6,"生物":7,"物理":8,"美术":32,"信息":33,"音乐":14,"体育":23,"道法":437}
subjectlistNum=[1,2,3,4,5,6,7,8,437,32,33,14,23]
subjectNamelist=["语文","数学","英语","化学（测试性功能）",'历史','地理','生物','物理','道法','美术','信息','音乐','体育']
####################################################### 
if len(arg)==3:
    if arg[1]=="yxpDCom":
        url="http://e.anoah.com/api_cache/?q=json/icom/Dcom/getDCom&info={\"dcom_id\":%s}"%arg[2]
        out=json.loads(requests.get(url).text)
        if "status" in out:
            text="指定的作业不存在"
        else:
            text="""优学派作业ID：%s    
创建时间：%s    
作业名称：%s    
作业标题：%s    
活动名称：%s    
描述：%s"""%(out["id"],out["create_time"],out["dcom_name"],out["dcom_title"],out["activity_name"],out["description"])
####################################################### 
    elif arg[1]=="yxpLt":
        textHave=0
        text="这是%s的所有作业评语：\n"%(yxpName(arg[2]))
        for j in range(0,len(subjectlistNum)):
            urlClassF="http://api2.anoah.com/jwt/homework/publish/getListForStudent?"\
                "user_id=%s&status=1&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=-1&pmatsemit=%s"%\
                (arg[2],subjectlistNum[j],yxpClassId(arg[2]),yxpTimeGet())
            outF=json.loads(requests.get(urlClassF).text)["recordset"]
            outFL=outF["lists"]
            for i in range(0,outF["total_count"]):
                if not outFL[i]["comment"]==None:
                    textHave=textHave+1
                    commentText=outFL[i]["comment"]["text"].replace("&nbsp;","")
                    text=text+outFL[i]["title"]+" "+outFL[i]["teacher_name"]+"\n老师评语："+commentText+"\n"
        if textHave==0:
            text=text+"无老师作业评语。"
#######################################################
    elif arg[1]=="yxpNm":
        cid=yxpClassId(arg[2])
        for i in range(0,len(cid))
            urlNm="https://e.anoah.com/api/?q=json/ebag/user/score/userClassRank&info={\"class_id\":\"%s\"}"%(cid[i])

#######################################################
    elif arg[1]=="yxpPic":
        url="https://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s"%(arg[2],yxpTimeGet())
        urlJson=json.loads(requests.get(url).text)["recordset"]["avatar"].replace(r"\/","/")
        urlPic="http://static.anoah.com"
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
        text=yxpName(arg[2])
#######################################################
    elif arg[1]=="yxpInfo":
        time=yxpTimeGet()
        urlHaoTiBen="https://e.anoah.com/api/?q=json/ebag5/Qtibook/readBookStatus&info="\
            "{\"start_time\":\"2008-08-08+00:00:00\",\"user_id\":%s}&pmatsemit=%s"%(arg[2],time)
        urlClass="https://e.anoah.com/api/?q=json/ebag5/User/getUserClasses&info={\"userid\":%s}&pmatsemit=%s"%(arg[2],time)
        urlScore="https://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s"%(arg[2],time)
        urlScore2="https://e.anoah.com/api/?q=json/ebag/user/score/score_count&info={\"userid\":%s}"%arg[2]
        urlScore3="https://e.anoah.com/api/?q=json/ebag/user/score/score_detail&info"\
            "={\"userid\":%s,\"pagesize\":10,\"page\":1,\"start\":\"\",\"end\":\"\"}&pmatsemit=%s"%(arg[2],time)
        HaoTi=json.loads(requests.get(urlHaoTiBen).text)
        Class=json.loads(requests.get(urlClass).text)
        ClassScore=""
        for t in range(0,len(Class["recordset"])):
            if t==0:
                ClassScore=Class["recordset"][t]["class_id"]
            else:
                ClassScore=str(ClassScore)+","+str(Class["recordset"][t]["class_id"])
        urlClassIn="https://api2.anoah.com/jwt/user/classes/subjects?class_id=%s&pmatsemit=%s"%(ClassScore,time)
        urlHomework="https://e.anoah.com/api/?q=json/ebag5/Homework/readHomeworkStat&info="\
            "{\"to\":\"\",\"class_ids\":\"%s\",\"user_id\":%s,\"from\":\"\"}&pmatsemit=%s"%(ClassScore,arg[2],time)
        Score=json.loads(requests.get(urlScore).text)
        Score2=json.loads(requests.get(urlScore2).text)
        Score3=json.loads(requests.get(urlScore3).text)
        ClassIn=json.loads(requests.get(urlClassIn).text)
        Homework=json.loads(requests.get(urlHomework).text)
        #---------------------------------------------
####################################################### 
elif len(arg)==2:
    if arg[1]=="yxpTIME": 
        text=yxpTimeGet()
    else:
        text="Error"
#######################################################
elif len(arg)==4:
    if arg[1]=="yxpRs":
        Classid=yxpClassId(arg[2])
        if(arg[3]=="最新"):
            text="这是 "+yxpName(arg[2])+"的全科最近分数（仅显示已批改）：\n"
            for i in range(0,13):
                url="http://e.anoah.com/api/?q=json/ebag5/Statistics/getStudentScoreInfo&info="\
                    "{\"user_id\":%s,\"class_id\":\"%s\",\"type\":0,\"subject_id\":%s,\"pagesize\":1,\"page\":1,\"start_date\":\"\",\"end_date\":\"\"}&pmatsemit=%s"%\
                        (arg[2],Classid,subjectlistNum[i],yxpTimeGet())
                out=json.loads(requests.get(url).text)
                if(out["recordset"]==""):
                    text=text+"☛ "+subjectNamelist[i]+"：无 已批改 成绩\n"
                else:
                    if(i in range(0,3)):
                        result=round(out["recordset"][0]["student_right_rate"]*120,2)
                        classr=round(out["recordset"][0]["class_right_rate"]*120,2)
                    else:
                        result=round(out["recordset"][0]["student_right_rate"]*100,2)
                        classr=round(out["recordset"][0]["class_right_rate"]*100,2)
                    if(result>=classr):
                        string="■"
                    else:
                        string="□"
                    text=text+"☛ "+subjectNamelist[i]+"："+out["recordset"][0]["publish_time"]+" "+out["recordset"][0]["title"]+"\n个人："+\
                        str(result)+"分（"+str(out["recordset"][0]["student_right_rate"])+"）\n全班平均分："+\
                        str(classr)+"分（"+str(out["recordset"][0]["class_right_rate"])+"）  "+string+"\n"
        #---------------------------------------------
        else:
            subjectNamelist=["语文","数学","英语","化学（测试性功能）",'历史','地理','生物','物理','道法','美术','信息','音乐','体育']
            url="http://e.anoah.com/api/?q=json/ebag5/Statistics/getStudentScoreInfo&info="\
                    "{\"user_id\":%s,\"class_id\":\"%s\",\"type\":0,\"subject_id\":%s,\"pagesize\":-1,\"page\":1,\"start_date\":\"\",\"end_date\":\"\"}&pmatsemit=%s"%\
                    (arg[2],Classid,subjectList[arg[3]],yxpTimeGet())
            out=json.loads(requests.get(url).text)
            if(subjectList[arg[3]] in range(1,4)):
                scoreMain=120
            else:
                scoreMain=100
            text="这是 "+yxpName(arg[2])+"的%s最近分数（仅显示已批改）：\n"%(arg[3])
            for i in range(0,len(out["recordset"])):
                if(out["recordset"]==""):
                    text=text+"☛ "+subjectNamelist[i]+"：无 已批改 成绩\n"
                else:
                    if(i in range(0,3)):
                        result=round(out["recordset"][i]["student_right_rate"]*scoreMain,2)
                        classr=round(out["recordset"][i]["class_right_rate"]*scoreMain,2)
                    else:
                        result=round(out["recordset"][i]["student_right_rate"]*scoreMain,2)
                        classr=round(out["recordset"][i]["class_right_rate"]*scoreMain,2)
                    if(result>=classr):
                        string="■"
                    else:
                        string="□"
                    text=text+str(i)+"  "+out["recordset"][i]["publish_time"]+" "+out["recordset"][i]["title"]+"\n个人："+\
                        str(result)+"分（"+str(out["recordset"][i]["student_right_rate"])+"）\n全班平均分："+\
                        str(classr)+"分（"+str(out["recordset"][i]["class_right_rate"])+"）  "+string+"\n"
#######################################################
    elif arg[1]=="yxpAs":
        classname=arg[3][:2]
        classIndex=arg[3][2:]
        urlClassF="http://api2.anoah.com/jwt/homework/publish/getListForStudent?"\
            "user_id=%s&status=0&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=-1&pmatsemit=%s"%\
            (arg[2],subjectList[classname],yxpClassId(arg[2]),yxpTimeGet())
        outF=json.loads(requests.get(urlClassF).text)["recordset"]["lists"][int(classIndex)-1]["course_hour_publish_id"]
        urlClassid="http://api2.anoah.com/jwt/homework/stat/basicForStudent?"\
            "user_id=%s&publish_id=%s&pmatsemit=%s"%(arg[2],outF,yxpTimeGet())
        outQid=json.loads(requests.get(urlClassid).text)["recordset"]
        answer=""
        Ut=False
        number=0
        text="这是%s的作业答案：\n不建议滥用\n"%(outQid["title"])
        #---------------------------------------------
        for csid in range(0,outQid["course_resource_count"]):
            if(outQid["course_resource_list"][csid]["icom_name"]=="互动试题"):
                Qid=outQid["course_resource_list"][csid]["qti_id"]
                urlAnswer="http://e.anoah.com/api_cache/?q=json/Qti/get&info="\
                    "{\"param\":{\"qid\":\"test:%s\",\"dataType\":1},\"pulishId\":\"%s\"}"%(Qid,outF)
                urlAnswerUt="http://e.anoah.com/api_cache/?q=json/Qti/get&info="\
                    "{\"param\":{\"qid\":\"%s\",\"dataType\":1},\"pulishId\":\"%s\"}"%(Qid,outF)
                outAnswer=json.loads(requests.get(urlAnswer).text)
                if outAnswer==[]:
                    outAnswer=json.loads(requests.get(urlAnswerUt).text)
                    Ut=True
                    fori=1
                else:
                    outAnswer=outAnswer["section"][0]["items"]
                    Ut=False
                    fori=len(outAnswer)
                for i in range(0,fori):
                    number=number+1
                    if not Ut:
                        items=outAnswer[i]
                    else:
                        items=outAnswer
                    textP=yxpToText(items["prompt"])
                    if "answer" in items:
                        if (len(textP)>10):
                            text=text+str(number)+" "+textP[:10]+" ..."+"-> "
                        else:
                            text=text+str(number)+" "+textP[:10]+"-> "
                        if isinstance(items["answer"],str):
                            answer=yxpToText(items["answer"])
                            text=text+answer+"\n"
                        else:
                            answerL=""
                            for j in items["answer"]:
                                answerL=answerL+j[0]
                                if not j==items["answer"][-1]:
                                    answerL=answerL+"，"
                            text=text+answerL+"\n"
                    #---------------------------------------------
                    else:
                        for j in range(0,len(items["items"])):
                            try:
                                textP=yxpToText(items["items"][j]["prompt"])
                            except:
                                textP=""
                            if isinstance(items["items"][j]["answer"],str):
                                answer=yxpToText(items["items"][j]["answer"])
                            else:
                                answer=""
                                for k in items["items"][j]["answer"]:
                                    answer=answer+k[0]
                                    if not k==items["items"][j]["answer"][-1]:
                                        answer=answer+"，"
                            if (len(textP)>10):
                                text=text+str(number)+"."+str(j+1)+" "+textP[:10]+"..."+"-> "+answer+"\n"
                            else:
                                text=text+str(number)+"."+str(j+1)+" "+textP[:10]+"-> "+answer+"\n"

#######################################################
    elif arg[1]=="yxpHw":
        time=yxpTimeGet()
        #---------------------------------------------
        if(arg[3]=="没写"):
            urlN="http://api2.anoah.com/jwt/homework/publish/getUndoNumForStudent?"\
                    "user_id=%s&class_id=%s&from_date=&to_date=&pmatsemit=%s"%\
                    (arg[2],yxpClassId(arg[2]),yxpTimeGet())
            outN=json.loads(requests.get(urlN).text)["recordset"]
            text="这是 %s 的没写作业：\n"%(yxpName(arg[2]))
            n=0
            for i in range(0,len(outN)):
                urlNok="http://api2.anoah.com/jwt/homework/publish/getListForStudent?"\
                    "user_id=%s&status=0&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=-1&pmatsemit=%s"%\
                    (arg[2],outN[i]["edu_subject_id"],yxpClassId(arg[2]),time)
                outNok=json.loads(requests.get(urlNok).text.encode("utf-8").decode("unicode_escape"))
                outNok=outNok["recordset"]
                if  (outN[i]["edu_subject_id"]==1  ):subjectId="语文" #
                elif(outN[i]["edu_subject_id"]==2  ):subjectId="数学" #
                elif(outN[i]["edu_subject_id"]==3  ):subjectId="英语" #
                elif(outN[i]["edu_subject_id"]==5  ):subjectId="历史" #
                elif(outN[i]["edu_subject_id"]==6  ):subjectId="地理"
                elif(outN[i]["edu_subject_id"]==7  ):subjectId="生物" #
                elif(outN[i]["edu_subject_id"]==8  ):subjectId="物理"
                elif(outN[i]["edu_subject_id"]==32 ):subjectId="美术"
                elif(outN[i]["edu_subject_id"]==33 ):subjectId="信息"
                elif(outN[i]["edu_subject_id"]==14 ):subjectId="音乐"
                elif(outN[i]["edu_subject_id"]==23 ):subjectId="体育"
                elif(outN[i]["edu_subject_id"]==437):subjectId="道法"
                for j in range(0,outN[i]["undo"]):
                    n=n+1
                    text=text+str(j+1)+" "+subjectId+" "+outNok["lists"][j]["title"]+" "+outNok["lists"][j]["teacher_name"]+"\n"
            text=text+"共%s个未写作业。\n可使用 yxp答案 [用户id] [科目] [作业前数字] 查看这个作业的答案"%str(n)
            #---------------------------------------------
        else:
            urlNOK="http://api2.anoah.com/jwt/homework/publish/getListForStudent?"\
                "user_id=%s&status=0&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=20&pmatsemit=%s"%\
                (arg[2],subjectList[arg[3]],yxpClassId(arg[2]),time)
            urlOk="http://api2.anoah.com/jwt/homework/publish/getListForStudent?"\
                "user_id=%s&status=1&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=20&pmatsemit=%s"%\
                (arg[2],subjectList[arg[3]],yxpClassId(arg[2]),time)
            ok=json.loads(requests.get(urlOk).text.encode('utf-8').decode("unicode_escape"))
            nok=json.loads(requests.get(urlNOK).text.encode('utf-8').decode("unicode_escape"))
            if(ok["status"]==0):
                text=ok["msg"]
            else:
            #---------------------------------------------
                okjs=ok["recordset"]
                nokjs=nok["recordset"]
                text="这是"+yxpName(arg[2])+"的"+arg[3]+"作业情况：\n"
                lists=okjs["lists"]
                noklists=nokjs["lists"]
                write=1
                if(okjs["total_count"]==0):
                    text="没有写了的作业。\n"
                    write=0
                else:
                    if(int(okjs["total_count"])>int(okjs["per_page"])):
                        rg=okjs["per_page"]
                    else:
                        rg=okjs["total_count"]
                    for i in range(0,int(rg)):
                        if i==0:
                            text=text+"☛ 写了的作业（%s个）：\n"%(okjs["total_count"])
                        text=text+lists[i]["start_time"]+" "+lists[i]["title"]+" "+lists[i]["subject_name"]+lists[i]["teacher_name"]#+"\n作业ID："+lists[i]["course_hour_publish_id"]
                        if not i==int(okjs["total_count"]):
                            text=text+"\n"
                    if (int(okjs["per_page"])<int(okjs["total_count"])):
                        text=text+"※ 仅显示%s个，但一共有%s个作业完成\n"%(okjs["per_page"],okjs["total_count"])
                if(nokjs["total_count"]==0):
                    if(write==0):
                        text="老师没留过作业。"
                    else:
                        text=text+"没有没写的作业。"
                else:
                    if(int(nokjs["total_count"])>int(nokjs["per_page"])):
                        rg=nokjs["per_page"]
                    else:
                        rg=nokjs["total_count"]
                    for i in range(0,int(rg)):
                        if i==0:
                            text=text+"☛ 没写的作业（%s个）：\n"%(nokjs["total_count"])
                        text=text+noklists[i]["start_time"]+" "+noklists[i]["title"]+" "+noklists[i]["subject_name"]+noklists[i]["teacher_name"]#+"\n作业ID："+noklists[i]["course_hour_publish_id"]
                        if not i==int(okjs["total_count"]):
                            text=text+"\n"
                    if (int(nokjs["per_page"])<int(nokjs["total_count"])):
                        text=text+"※ 仅显示%s个，但一共有%s个作业未完成"%(nokjs["per_page"],nokjs["total_count"])
#######################################################
else:
    text="参数不够"
####################################################### 
with open(r"D:\Program Source\QQBOT\python\Temp\temp.txt","w+",encoding="UTF-8") as f:
    if(is_pydroid):print(text)
    else:
            text=str(text)
            f.write(text)
            print(text)

