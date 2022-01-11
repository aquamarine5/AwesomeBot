# AwesomeBot
*（原ebagqbot，先已拆分为YouxuepaiUtil和AwesomeBot）  
关于YouxuepaiUtil（优学派）的更多信息，请跳转至[YouxuepaiUtil](github.com/awesomehhhhh/YouxuepaiUtil)库*  
[![GitHub repo size](https://img.shields.io/github/repo-size/awesomehhhhh/AwesomeBot)](https://github.com/awesomehhhhh/AwesomeBot)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/awesomehhhhh/AwesomeBot)]()
[![Last commit](https://img.shields.io/github/last-commit/awesomehhhhh/AwesomeBot)]()
![Visitor](https://visitor-badge.glitch.me/badge?page_id=AwesomeBot)

**阿巴阿巴阿巴巴巴巴**

> ebag yxp代码：[webyxp.py](https://github.com/awesomehhhhh/EbagUtil)  
> 网络爬虫 代码：webapi.py  
> qqbot机器人实现：main.kt  
> qqbot基于：[mirai](https://github.com/mamoe/mirai)
## 使用须知：
- **AwesomeBot 在2021/09/11进行重写，敬请期待。**
## 使用方法：

### [webapi.py](python/webapi.py)

- 在[这个](.github/workflows/python-package.yml)Github Actions的yml内有一些使用例子，仅需要取消`--diswrite-file`即可

## （webapi）正在（计划）实现：  

**指已获取到对应api或准备beautifulsoup解析**
- [ ] 翻译（360，阿里，彩云小译，搜狗） 
- [ ] 百度热搜  
- [ ] 360指数（一个专业一个广泛）
- [ ] 翻 译 生 草 机 （翻译20次）  
- [ ] 搜歌  
- [ ] QQ头像爬虫（随机头像）  
- [ ] ffmpeg语音倒放（mirai 1.2.1 silk）  
- [ ] tts转语音（voice sdk）  
- [ ] b站视频解析（封面，mp4直链）  

## （webapi）已经实现：

- [X] 拼多多买东西（[Py](python/webapi.py#L346)，[Kt](src/main/kotlin/main.kt#L168)）（图片+文字描述，暂无链接）（仅用于观察营销号题目和图片用）
- [X] 图片识别（[Py](python/webapi.py#L280)，[Kt1](src/main/kotlin/main.kt#L66)，[Kt2](src/main/kotlin/main.kt#L157)）
- [X] 实时监测群内大于50次的消息是否存在广告、灌水等并t出（[Py](python/webapi.py#L379)，[Kt](src/main/kotlin/main.kt#L318)）
- [X] 作业帮搜题（[Py](python/webapi.py#L296)，[Kt](src/main/kotlin/main.kt#L120)）（仅文字）（支持图文发送）  
- [X] 最近新闻（百度指数）  
- [X] 百度智能搜索（连百度百科）  
- [X] b站头像爬虫（随机头像）  
- [X] b站热词（[Py](python/webapi.py#L371)，[Kt](src/main/kotlin/main.kt#L181)）  
- [X] 每日亿图（锁屏杂志）（多主题已支持）  
- [X] 搜索建议  
- [X] 翻译  
- [X] 翻译单词（爱词霸）  
- [X] 热点分析（微博）  
- [X] 翻译文言文（百度）  
- [X] 根据经纬度确定位置（百度地图）  
- [X] 根据IP看地点  

## webapi.py中使用到的API来源
- 翻译：[百度翻译开放平台](https://api.fanyi.baidu.com/api/trans/product/index)，[py-googletrans](https://github.com/ssut/py-googletrans)  
- 热搜：微博  
- 热词：B站  
- 搜索建议：百度、必应、360、搜狗  
- 锁屏杂志（图片）：OPPO（乐划锁屏）  
- and more...
## 关于webyxp
详见[此repo](https://github.com/awesomehhhhh/EbagUtil)
