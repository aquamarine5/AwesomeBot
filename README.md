# ebagqbot
阿巴阿巴阿巴巴巴巴

ebag yxp代码：webyxp.py  
爬虫 代码：webapi.py  
qqbot机器人实现：main.kt  

## （webyxp）功能&使用介绍：  

- python webyxp.py yxpRs 1585745 最新  
看这个id的最新已批改成绩和班级平均分比较  
- python webyxp.py yxpRs 1585745 生物  
看这个id的所有生物已批改成绩和班级平均分比较
- python webyxp.py yxpLt 1585733  
看这个id的所有科目的老师作业评语
- python webyxp.py yxpAs 1585745 语文4  
看这个id下语文的第4个没写作业的答案  
（请勿滥用）  
- python webyxp.py yxpPic 1585745  
看这个id的私人头像（见\Temp）
- python webyxp.py yxpInfo 1585745  
看这个id的信息（信息大杂烩）
- python webyxp.py yxpHw 1585745 没写  
所有没写的作业
- python webyxp.py yxpHw 1585745 语文  
语文没写的作业
- python webyxp.py yxpNm 1585745  
看积分排行榜和积分分布情况
- python webyxp.py yxpCt 1585745  
看课程表  
- python webyxp.py yxpBk 1585745  
看所用书籍并保存第一张课本图片（见\Temp\Image）  

## 脚本需要在cmd下运行，或者把 is_pydroid设置 true然后在arg下写命令。

## （webyxp）如果有时间就实现：

- [ ] 看通知  
- [ ] 每日一题（取好题/错题本信息）
- [ ] 看所有作业的分数而不局限于已批改  
- [ ] 作业互评  

## （webyxp）暂时无法实现：  

需要获取与uid所关联的设备id的api但没有找到  
- [ ] id所在学校  
- [ ] 根据id看允许下载的应用  

## （webapi）正在实现：  

- [ ] 每日一图（杂志锁屏）（protobuf解析）  
- [ ] 翻译（百度，360，阿里，彩云小译，搜狗） 
- [ ] 翻译文言文（百度）  
- [ ] 翻 译 生 草 机 （翻译20次）  
- [ ] 搜歌  
- [ ] ffmpeg语音倒放（mirai 1.2.1 silk）  
- [ ] tts转语音（voice sdk）  
- [ ] b站视频解析（封面，mp4直链）  
- [ ] 微博热点分析

## （webapi）已经实现：

- [X] 搜索建议（百度，必应，360，搜狗搜索）  
- [X] 翻译（谷歌翻译）  
- [X] 翻译单词（爱词霸）  
- [X] 根据经纬度确定位置（百度地图）  
- [X] 根据IP看地点  

## （func.py）计划：

- [ ] 整合进webapi.py（但因为内容未涉及到爬虫可能搁置）
