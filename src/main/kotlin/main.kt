import net.mamoe.mirai.Bot
import net.mamoe.mirai.alsoLogin
import net.mamoe.mirai.event.*
import net.mamoe.mirai.join
import net.mamoe.mirai.message.*
import net.mamoe.mirai.message.data.*
import net.mamoe.mirai.contact.PermissionDeniedException
import kotlinx.coroutines.InternalCoroutinesApi
import net.mamoe.mirai.contact.Member
import net.mamoe.mirai.utils.BotConfiguration
import java.io.*
import java.lang.Exception
import java.lang.IndexOutOfBoundsException

const val program="\"d:/Program Source/QQBOT/python/webyxp.py\""
const val webapi="\"d:/Program Source/QQBOT/python/webapi.py\""
const val func="\"d:/Program Source/QQBOT/python/func.py\""
const val image="\"d:/Program Source/QQBOT/python/image.py\""
const val temp="D:/Program Source/QQBOT/python/Temp/temp.txt"
const val elog="D:/Program Source/QQBOT/python/Temp/t.log"
const val tempCheck="D:/Program Source/QQBOT/python/Temp/check.txt"
const val imageTemp="D:/Program Source/QQBOT/python/Temp/temp.jpg"
const val imageMath="D:/Program Source/QQBOT/python/Temp/Math.png"
const val imagePrivate="D:/Program Source/QQBOT/python/Temp/FacePrivate.jpg"

@InternalCoroutinesApi
suspend fun main() {

    val qqId = 924410958L//Bot的QQ号，需为Long类型，在结尾处添加大写L
    val password = File("D:/Program Source/QQBOT/password.txt").readText()//Bot的密码
    val miraiBot = Bot(qqId, password){
        fileBasedDeviceInfo("device.json")
        protocol=BotConfiguration.MiraiProtocol.ANDROID_PHONE
    }.alsoLogin()
    var type=1
    var photopath=""
    var command=""
    //miraiBot.getGroup(970111459L).sendMessage("机器人 on")
    //miraiBot.getGroup(830875502L).sendMessage("机器人 on").recallIn(10000)
    //miraiBot.getGroup(830875502L).sendMessage("https://github.com/awesomehhhhh/AwesomeBot").recallIn(10000)
    //miraiBot.getGroup(830875502L).sendMessage("Debug Note:不会踢人了*暂时*").recallIn(10000)
    miraiBot.subscribeAlways<MessageEvent> { event ->
        type=1
        print(event.message[Image]?.queryUrl()+"\n")
        try{
           val message = event.message.content
           check(event)
           if(message=="机器人 off"){
                reply(At(event.sender as Member)+" 呜呜呜有人要关我")
                return@subscribeAlways
            }
            else{
            event.message[Image]?.queryUrl()
            val ct = message.split(" ")
            when (ct[0]) {
                "yxpLt", "yxp老师评语" -> {
                    command = "python $program yxpLt ${ct[1]}"
                }
                "数学题", "math" -> {
                    type=2

                    command = "python $webapi math"
                    photopath=imageMath
                }
                "zyb","作业帮","作业"->{
                    type=0
                    var num=-1
                    num = if (ct.size==2){
                        0
                    } else{
                        ct[2].toInt()
                    }
                    val msg="python $webapi zyb ${ct[1]} $num".execute().waitForThis().inputStream.readString().split("{img}")
                    buildMessageChain {
                        if(msg.size==1){
                            add(msg[0])
                        }
                        else{
                        for ((index,m) in msg.withIndex())
                            {
                                add(m)
                                if(msg.size!=(index+1)){
                                    add(uploadImage(File("D:\\Program Source\\QQBOT\\python\\Temp\\Study\\$index.jpg")))
                                }

                            }
                        }
                    }.send()
                }
                "yxpInfo", "yxp信息" -> {
                    command = "python $program yxpInfo ${ct[1]}"
                }
                "yxpNm", "yxp积分" -> {
                    command = "python $program yxpNm ${ct[1]}"
                }
                "yxpPRs", "yxpPrs", "yxp批改成绩", "yxpRs" -> {
                    command = "python $program yxpRs ${ct[1]} ${ct[2]}"
                }
                "yxpAs", "yxp答案" -> {
                    command = "python $program yxpAs ${ct[1]} ${ct[2]}${ct[3]}"
                }
                "yxpPic", "yxppic", "yxp照片" -> {
                    type=0
                    command = "python $program yxpPic ${ct[1]}"
                    val rt=command.execute()
                    rt.waitFor()
                    val file = File(temp)
                    if (file.readText() == "") {
                        reply("用户不存在")
                        println("ct[0]")
                    } else {
                        buildMessageChain {
                            add("这是 优学派用户 e${ct[1].toInt()}（${file.readText()}） 的头像\n")
                            add(uploadImage(File(imagePrivate)))
                        }.send()
                    }
                }
                "yxpHW", "yxp作业", "yxpHw", "yxp作业完成" -> {
                    if (ct.size == 3) {
                        when (ct[2]) {
                            "语文", "数学", "英语", "历史", "道法", "生物", "地理", "信息", "物理", "体育", "美术", "音乐", "没写" -> {
                                command = "python $program yxpHw ${ct[1]} ${ct[2]}"
                            }
                            else -> {
                                type=0
                                reply("科目不对，仅支持：语文，数学，英语，历史，道法，生物，地理，信息，物理，体育，美术，音乐")
                            }
                        }
                    } else {
                        type=0
                        reply("给的东西不够或者多了，例子：yxp作业 1585745 生物")
                    }
                }
                "yxprd", "yxp随机", "yxpRand", "yxp随机作业" -> {
                    command = "python $program yxpDCom ${ct[1]}"
                }
                "eat" -> {
                    type=2
                    command = "python $image yz ${ct[1]}"
                    photopath=imageTemp
                }
                "trsWd", "翻译单词", "trswd" -> {
                    var engine = ""
                    engine = if (ct.size == 2) {
                        "-"
                    } else {
                        ct[2]
                    }
                    command = "python $webapi trsWd ${ct[1]} $engine"
                }
                "trsg","谷歌翻译","翻译谷歌","translate_google","翻译g"->{
                    if(ct.size==1){
                        reply("请输入翻译参数")
                        return@subscribeAlways
                    }
                    if(ct.size==2){
                        reply("请输入翻译语言")
                        return@subscribeAlways
                    }
                    command = "python $webapi trs ${ct[1]} g ${ct.dropLast(2).joinToString(" ")}"
                }
                "trs", "翻译", "translate" -> {
                    if(ct.size==1){
                        reply("请输入翻译参数")
                        return@subscribeAlways
                    }
                    if(ct.size==2){
                        reply("请输入翻译语言")
                        return@subscribeAlways
                    }
                    command = "python $webapi trs ${ct[1]} b ${ct.drop(2).joinToString(" ")}"
                }

                "搜索建议", "idea", "search" -> {
                    type=0
                    reply("python $webapi search ${ct[1]}".execute().waitForThis().inputStream.readString()).recallIn(60000)
                }
                "baidu","百度"->{
                    command = "python $webapi baidu ${ct[1]}"
                }
                "hotword","热词"->{
                    command = "python $webapi hotword"
                }
                "在？"->{reply("在")}
                "news","新闻"->{
                    command = "python $webapi news ${ct[1]}"
                }
                "face","头像"->{
                    type=0
                    val result="python $webapi face b".execute().waitForThis().inputStream.readString()
                    print("D:\\Program Source\\QQBOT\\python\\Temp\\Face\\${result.trim().toInt()}.jpg\n")
                    File("D:\\Program Source\\QQBOT\\python\\Temp\\Face\\${result.trim().toInt()}.jpg").sendAsImage()
                }
                "help", "帮助" -> {
                    type=0
                    if(ct.size == 1){
                    reply("""->括号内为简写如："搜索建议 机器人"可替换成"idea 机器人"<-
github.com/awesomehhhhh/AwesomeBot
翻译 需要翻译的文字 翻译的语种 -> 返回翻译结果（trs）
头像 ->返回某个b站头像（face）
热词 ->返回b站热词（hotword）
热搜 ->返回微博热搜（hot）
百度 内容 ->返回百度搜索的内容（测试中）（百度）
翻译单词 需要翻译的单词 -> 返回单词英文结果和相关信息（trsWd）
搜索建议 信息 ->返回搜索建议（idea）
帮助 ->返回帮助（help）
作业帮 题目 ->返回作业帮搜题（zyb）
新闻 内容 ->返回最近新闻（测试）（news）
性别判断 人名字 ->根据人名判断性别（ng）
eat 文字 ->生成表情包
二维码生成 内容 ->生成二维码（qrcode）（仅限英文）
数学题 ->返回数学题""".trimIndent())}
                    else if (ct.size == 2){
                        if(ct[1]=="谷歌翻译"){
                            reply("""支持的翻译语种：
（另：谷歌翻译服务器日常土豆）
简体中文，繁体中文，文言文，粤语，
日语，英语，德语，法语，韩语，芬兰语，犹太语，祖鲁语，南非语，希腊语，
孟加拉语，加泰罗尼亚语，保加利亚语，库尔德语，葡萄牙语，阿拉伯语
象形（阿姆哈拉文）
""".trimIndent())
                        }
                        else if(ct[1]=="百度翻译"){
                        reply("""
#支持的语种（即翻译关键字）：
 中文->粤语，粤语->中文（翻译关键字：粤语中文），文言文->中文（翻译关键字：文言文中文），中文->文言文
 韩语，葡萄牙语，阿拉伯语，荷兰语，英语，日语，德语，保加利亚语，希腊语
# 用法：
 翻译 [翻译关键字] [需要翻译的内容]
                        """.trimIndent())}
                        else if(ct[1]=="图片"){
                            reply("""
# 用法： 图片 [参数]
目前参数只能为数字（1-9）
不传参则随机
3是宠物，5是明星
其他暂时未知
                            """.trimIndent())
                        }
                        else if(ct[1]=="翻译"){
                            reply("请输入\"help 百度翻译\"或\"help 谷歌翻译\"")
                        }
                    }
                }
                "yxpHelp", "yxp帮助" -> {
                    reply("""
--优学派方面（快 没 用 了）--
yxp照片 uid ->返回uid对应的照片
yxp作业 uid 没写 ->返回uid所有没写作业
yxp答案 uid 学科 第几个 ->返回uid指定学科的没写作业的答案
yxp信息 uid ->返回uid对应信息
yxp积分 uid ->返回uid对应积分
yxp老师评语 uid ->返回uid作业评语""".trimIndent())
                }
                "ip" -> {
                    command = "python $webapi ip ${ct[1]}"
                }
                "pos" -> {
                    command = "python $webapi pos ${ct[1]}"
                }
                "qrcode", "二维码生成" -> {
                    type=0
                    val qrtext = message.replace("qrcode ", "").replace("二维码生成 ","")
                    "myqr $qrtext -d \"D:/Program Source/QQBOT/python/Temp\"".execute().waitFor()
                    photopath="D:/Program Source/QQBOT/python/Temp/qrcode.png"
                    File(photopath).sendAsImage()
                }
                "photo","图片","每日一图"->{
                    type=0
                    val index:Int = if(ct.size==1) -1;
                    else if(ct[1].length>=2){
                        reply("数字过大，仅支持1-9（包括1-9）")
                        print(3)
                        return@subscribeAlways
                    } else {
                        try{
                            ct[1].toInt()
                        }catch (e:Exception){
                            reply("参数不是数字")
                            return@subscribeAlways
                        }
                    }
                    print(1)
                    val f="python $webapi photo $index".execute().waitForThis().inputStream.readString().split("|")
                    print("python $webapi photo $index")
                    print(f)
                    try{
                        reply(f[1].replace("_", "\n"))
                        File(f[0]).sendAsImage()
                    }
                    catch(e:IndexOutOfBoundsException){
                        reply("你真倒霉")
                    }
                }
                "性别判断", "ng", "Sex" -> {
                    command = "python $func ng ${ct[1]}"
                }
                "hot","微博热搜","wb","微博" -> {
                    type=0
                    val file = File(temp)
                    reply("python $webapi hot".execute().waitForThis().inputStream.readString()).recallIn(30000)
                }
                else->{
                    type=100
                }
            }
            when (type){
                1->{
                    reply(command.execute().waitForThis().inputStream.readString())
                    type=0
                }
                2->{
                    command.execute().waitFor()
                    File(photopath).sendAsImage()
                    type=0
                }
            }
            }
        }catch(e:Exception){
            reply(e.toString())
            e.printStackTrace()
        }
    }

    miraiBot.join() // 等待 机器人 离线, 避免主线程退出
}

suspend fun check(event: MessageEvent){
    if(event.message.content.length<50)return
    if(event.message.content.contains("<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"))return
    if(event.sender.id== 2854196310L)return
    if((event.sender as Member).permission.level==1)return
    if(event.message.content.contains("bilibili.com"))return
    if(event.message.content.contains("docs.microsoft.com"))return
    if(event.message.content.contains("unity.cn"))return
    if(event.message.content.contains("unity.com"))return
    if(event.message.content.contains("csdn.com"))return
    if(event.message.content.contains("github.com"))return
    val result="python $webapi check \"${event.message.content}\"".execute().waitForThis().inputStream.readString()
    println(result)
    if(event.message.content.contains("感兴趣的可以加一下进去交流学习哦")) checkFailed(event,result)
    if (result.contains("通过")) print(result)
    else checkFailed(event,result)
}

suspend fun checkFailed(event: MessageEvent,result:String){
    try {
        //(event.sender as Member).kick("Bot测试")
    } catch (err: PermissionDeniedException) {
        event.reply(At(event.sender as Member) + "有违禁信息但权限原因无法踢走\n原因：$result")
    } finally {
        event.reply(At(event.sender as Member) + "有违禁信息\n原因：$result")
    }
    File(elog).writeText(File(elog).readText() + "\n" + event.senderName + " " + event.message.content)
}
fun String.execute(): Process {
    val runtime = Runtime.getRuntime()
    return runtime.exec(this)
}
fun Process.waitForThis():Process{
    this.waitFor()
    return this
}
fun InputStream.readString():String{
    val bos=ByteArrayOutputStream()
    try{
        val a=ByteArray(1)
        var len: Int
        do{
            len=this.read(a)
            bos.write(a)
        }while (-1!=len)
        return bos.toString("gbk").dropLast(1)
    }
    catch (e:Exception){
        e.printStackTrace()
        return e.toString()
    }
    finally {
        bos.close()
    }
}
