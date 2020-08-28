import net.mamoe.mirai.Bot
import net.mamoe.mirai.alsoLogin
import net.mamoe.mirai.event.*
import net.mamoe.mirai.join
import net.mamoe.mirai.message.*
import net.mamoe.mirai.message.data.*
import kotlinx.coroutines.InternalCoroutinesApi
import java.io.File
import java.lang.Exception
import java.nio.charset.Charset
import java.nio.charset.StandardCharsets


@InternalCoroutinesApi
suspend fun main() {

    val qqId = 924410958L//Bot的QQ号，需为Long类型，在结尾处添加大写L
    val password = File("D:/Program Source/QQBOT/password.txt").readText()//Bot的密码
    val miraiBot = Bot(qqId, password){
        fileBasedDeviceInfo("device.json")
    }.alsoLogin()

    val program="\"d:/Program Source/QQBOT/python/webyxp.py\""
    val webapi="\"d:/Program Source/QQBOT/python/webapi.py\""
    val func="\"d:/Program Source/QQBOT/python/func.py\""
    val image="\"d:/Program Source/QQBOT/python/image.py\""
    val temp="D:/Program Source/QQBOT/python/Temp/temp.txt"
    val imageTemp="D:/Program Source/QQBOT/python/Temp/temp.jpg"
    val imageMath="D:/Program Source/QQBOT/python/Temp/Math.png"
    val imagePrivate="D:/Program Source/QQBOT/python/Temp/FacePrivate.jpg"
    var type=1
    var photopath=""
    var command=""
    miraiBot.subscribeAlways<MessageEvent> { event ->
        type=1
        try{
            val message = event.message.content
            //event.message[Image]?.queryUrl()
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
                    command = "python $webapi zyb ${ct[1]} $num"
                    println(command)
                    val rt=command.execute()
                    rt.waitFor()
                    val msg=File(temp).readText(StandardCharsets.UTF_8).split("{img}")
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
                "trs", "翻译", "translate" -> {
                    var engine = ""
                    var dest = "zh-cn"
                    engine = if (ct.size == 3) {
                        "-"
                    } else {
                        ct[3]
                    }
                    if (ct.size == 2) {
                        engine = "-"
                    } else {
                        dest = ct[2]
                    }
                    command = "python $webapi trs ${ct[1]} $dest $engine"
                }
                "搜索建议", "idea", "search" -> {
                    command = "python $webapi search ${ct[1]}"
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
                    type=2
                    command = "python $webapi face -"
                    photopath="D:\\Program Source\\QQBOT\\python\\Temp\\face.png"
                }
                "help", "帮助" -> {
                    type=0
                    if(ct.size == 1){
                    reply("""->括号内为简写如："搜索建议 机器人"可替换成"idea 机器人"<-
github.com/awesomehhhhh/ebagqbot
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
                    else if (ct.size == 2){reply("""支持的翻译语种：
简体中文，繁体中文，文言文，粤语，
日语，英语，德语，法语，韩语，芬兰语，犹太语，祖鲁语，南非语，希腊语，
孟加拉语，加泰罗尼亚语，保加利亚语，库尔德语，葡萄牙语，阿拉伯语
象形（阿姆哈拉文）
""")}
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
                    val rt=command.execute()
                    rt.waitFor()
                    command = "myqr $qrtext -d \"D:/Program Source/QQBOT/python/Temp\""
                    photopath="D:/Program Source/QQBOT/python/Temp/qrcode.png"
                }
                "photo","图片","每日一图"->{
                    type=0
                    command = "python $webapi photo"
                    val rt=command.execute()
                    rt.waitFor()
                    val f=File(temp).readText().split("|")
                    File(f[0]).sendAsImage()
                    reply(f[1])
                }
                "性别判断", "ng", "Sex" -> {
                    command = "python $func ng ${ct[1]}"
                }
                "hot","微博热搜","wb","微博" -> {
                    command = "python $webapi hot"
                }
                "resend" -> {
                    type=0
                    when (ct[1]) {
                        "text" -> {
                            try {
                                val file = File(temp)
                                reply(file.readText())
                            } catch (e: Exception) {
                                reply(e.toString())
                            }
                        }
                        "image" -> {
                            try {
                                File(imageTemp).sendAsImageTo(subject)
                            } catch (e: Exception) {
                                reply(e.toString())
                            }
                        }
                    }
                }
                else->{
                    type=100
                    println(666)
                }
            }
            println(type)
            when (type){
                1->{
                    val rt=command.execute()
                    rt.waitFor()
                    reply(File(temp).readText())
                    type=0
                }
                2->{
                    val rt=command.execute()
                    rt.waitFor()
                    File(photopath).sendAsImage()
                    type=0
                }
            }
        }catch(e:Exception){reply(e.toString())}
    }
    miraiBot.join() // 等待 Bot 离线, 避免主线程退出
}
fun String.execute(): Process {
    val runtime = Runtime.getRuntime()
    return runtime.exec(this)
}
