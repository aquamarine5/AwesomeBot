import net.mamoe.mirai.Bot
import net.mamoe.mirai.alsoLogin
import net.mamoe.mirai.event.*
import net.mamoe.mirai.join
import net.mamoe.mirai.message.*
import net.mamoe.mirai.message.data.*
import net.mamoe.mirai.contact.PermissionDeniedException
import kotlinx.coroutines.InternalCoroutinesApi
import net.mamoe.mirai.contact.Member
import net.mamoe.mirai.event.events.BotInvitedJoinGroupRequestEvent
import net.mamoe.mirai.event.events.NewFriendRequestEvent
import net.mamoe.mirai.utils.BotConfiguration
import java.io.*
import java.lang.Exception
import java.lang.IndexOutOfBoundsException

const val program = "\"d:/Program Source/QQBOT/python/webyxp.py\""
const val webapi = "\"d:/Program Source/QQBOT/python/webapi.py\""
const val func = "\"d:/Program Source/QQBOT/python/func.py\""
const val image = "\"d:/Program Source/QQBOT/python/image.py\""
const val temp = "D:/Program Source/QQBOT/python/Temp/temp.txt"
const val elog = "D:/Program Source/QQBOT/python/Temp/t.log"
const val imageTemp = "D:/Program Source/QQBOT/python/Temp/temp.jpg"
const val imageMath = "D:/Program Source/QQBOT/python/Temp/Math.png"
const val imagePrivate = "D:/Program Source/QQBOT/python/Temp/FacePrivate.jpg"

enum class MessageType {
    CodeDefineBySelf, Common, Image
}

@InternalCoroutinesApi
suspend fun main() {

    val qqId = 924410958L//Bot的QQ号，需为Long类型，在结尾处添加大写L
    val password = File("D:/Program Source/QQBOT/password.txt").readText()//Bot的密码
    val miraiBot = Bot(qqId, password) {
        fileBasedDeviceInfo("device.json")
        protocol = BotConfiguration.MiraiProtocol.ANDROID_PHONE
    }.alsoLogin()
    var type: MessageType?
    var photopath = ""
    var command:String?=null
    miraiBot.getGroup(1074494974L).sendMessage("qq bot start on all group,and will recall in 10 second.").recallIn(30000)
    miraiBot.getGroup(830875502L).sendMessage("qq bot start on all group,and will recall in 10 second.").recallIn(30000)
    miraiBot.getGroup(1074494974L).sendMessage("https://github.com/awesomehhhhh/AwesomeBot").recallIn(30000)
    miraiBot.getGroup(830875502L).sendMessage("https://github.com/awesomehhhhh/AwesomeBot").recallIn(30000)
    miraiBot.getGroup(1019390914L).sendMessage("qq bot start on all group,and will recall in 10 second.").recallIn(30000)
    miraiBot.getGroup(1019390914L).sendMessage("https://github.com/awesomehhhhh/AwesomeBot").recallIn(30000)

    miraiBot.subscribeAlways<BotInvitedJoinGroupRequestEvent> { event ->
        event.accept()
    }
    miraiBot.subscribeAlways<NewFriendRequestEvent> { event ->
        event.accept()
    }
    miraiBot.subscribeAlways<MessageEvent> { event ->
        type = MessageType.Common
        print(event.message[Image]?.queryUrl() + "\n")
        if ((event.sender as Member).group.id == 859089296L) return@subscribeAlways
        try {
            val message = event.message.content
            if (!check(event)) return@subscribeAlways
            if (message == "机器人 off") {
                reply(At(event.sender as Member) + " 呜呜呜有人要关我")
                return@subscribeAlways
            } else {
                val ct = message.split(" ")
                when (ct[0]) {
                    "yxpLt", "yxp老师评语" -> command = "python $program yxpLt ${ct[1]}"
                    "yxpInfo", "yxp信息" -> command = "python $program yxpInfo ${ct[1]}"
                    "yxpNm", "yxp积分" -> command = "python $program yxpNm ${ct[1]}"
                    "yxpPRs", "yxpPrs", "yxp批改成绩", "yxpRs" -> command = "python $program yxpRs ${ct[1]} ${ct[2]}"
                    "yxpAs", "yxp答案" -> command = "python $program yxpAs ${ct[1]} ${ct[2]}${ct[3]}"
                    "给张泉铭一个相遇之缘" -> {
                        type = MessageType.CodeDefineBySelf
                        reply("爬")
                    }
                    "yxpPic", "yxppic", "yxp照片" -> {
                        type = MessageType.CodeDefineBySelf
                        "python $program yxpPic ${ct[1]}".execute().waitFor()
                        val file = File(temp).readText()
                        if (file == "") {
                            reply("用户不存在")
                            println("ct[0]")
                        } else {
                            buildMessageChain {
                                add("这是 优学派用户 e${ct[1].toInt()}（$file） 的头像\n")
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
                                    type = MessageType.CodeDefineBySelf
                                    reply("科目不对，仅支持：语文，数学，英语，历史，道法，生物，地理，信息，物理，体育，美术，音乐")
                                }
                            }
                        } else {
                            type = MessageType.CodeDefineBySelf
                            reply("给的东西不够或者多了，例子：yxp作业 1585745 生物")
                        }
                    }
                    "yxprd", "yxp随机", "yxpRand", "yxp随机作业" -> command = "python $program yxpDCom ${ct[1]}"
                    "eat" -> {
                        type = MessageType.Image
                        command = "python $image yz ${ct[1]}"
                        photopath = imageTemp
                    }
                    "数学题", "math" -> {
                        type = MessageType.Image
                        command = "python $webapi math"
                        photopath = imageMath
                    }
                    "zyb", "作业帮", "作业" -> {
                        type = MessageType.CodeDefineBySelf
                        val num = if (ct.size == 2) 0 else ct[2].toInt()
                        val msg = "python $webapi zyb ${ct[1]} $num".runExecute().split("{img}")
                        buildMessageChain {
                            if (msg.size == 1) {
                                add(msg[0])
                            } else {
                                for ((index, m) in msg.withIndex()) {
                                    add(m)
                                    if (msg.size != (index + 1)) {
                                        add(uploadImage(File("D:\\Program Source\\QQBOT\\python\\Temp\\Study\\$index.jpg")))
                                    }

                                }
                            }
                        }.send()
                    }
                    "trsWd", "翻译单词", "trswd" -> {
                        val engine: String = if (ct.size == 2) {
                            "-"
                        } else {
                            ct[2]
                        }
                        command = "python $webapi trsWd ${ct[1]} $engine"
                    }
                    "trsg", "谷歌翻译", "翻译谷歌", "translate_google", "翻译g" -> {
                        if (ct.size == 1) {
                            reply("请输入翻译参数")
                            return@subscribeAlways
                        }
                        if (ct.size == 2) {
                            reply("请输入翻译语言")
                            return@subscribeAlways
                        }
                        command = "python $webapi trs ${ct[1]} g ${ct.dropLast(2).joinToString(" ")}"
                    }
                    "trs", "翻译", "translate" -> {
                        if (ct.size == 1) {
                            reply("请输入翻译参数")
                            return@subscribeAlways
                        }
                        if (ct.size == 2) {
                            reply("请输入翻译语言")
                            return@subscribeAlways
                        }
                        command = "python $webapi trs ${ct[1]} b ${ct.drop(2).joinToString(" ")}"
                    }
                    "shop", "买东西", "商品", "拼多多" -> {
                        type = MessageType.CodeDefineBySelf
                        val r = "python $webapi shop".runExecute().split("|")
                        print(r)
                        reply("${r[0]}${r[1]}")
                        if ((event.sender as Member).group.id != 830875502L) File("D:\\Program Source\\QQBOT\\python\\Temp\\shop.jpg").sendAsImage()
                    }
                    "搜索建议", "idea", "search" -> {
                        type = MessageType.CodeDefineBySelf
                        reply("python $webapi search ${ct[1]}".runExecute()).recallIn(60000)
                    }

                    "baidu", "百度" -> command = "python $webapi baidu ${ct[1]}"
                    "hotword", "热词" -> command = "python $webapi hotword"
                    "在？" -> reply("在")
                    "news", "新闻" -> command = "python $webapi news ${ct[1]}"
                    "face", "头像" -> {
                        type = MessageType.CodeDefineBySelf
                        val result = "python $webapi face b".runExecute()
                        print("D:\\Program Source\\QQBOT\\python\\Temp\\Face\\${result.trim().toInt()}.jpg\n")
                        try {
                            File("D:\\Program Source\\QQBOT\\python\\Temp\\Face\\${result.trim().toInt()}.jpg").sendAsImage()
                        } catch (e: IllegalStateException) {
                            reply("图片发送失败，原因：网速过慢\n你可以资助我来使网速更快：")
                        }
                    }
                    "help", "帮助" -> {
                        type = MessageType.CodeDefineBySelf
                        if (ct.size == 1) {
                            File("D:\\Program Source\\QQBOT\\docs\\help.png").sendAsImage()
                            /*
                            reply("""->括号内为简写如："搜索建议 机器人"可替换成"idea 机器人"<-
github.com/awesomehhhhh/AwesomeBot
翻译 需要翻译的文字 翻译的语种 -> 返回翻译结果（trs）
头像 ->返回某个b站头像（face）
热词 ->返回b站热词（hotword）
热搜 ->返回微博热搜（hot）
百度 内容 ->返回百度搜索的内容（测试中）（百度）""".trimIndent()).recallIn(30000)
                            reply("""翻译单词 需要翻译的单词 -> 返回单词英文结果和相关信息（trsWd）
搜索建议 信息 ->返回搜索建议（idea）
帮助 ->返回帮助（help）
作业帮 题目 ->返回作业帮搜题（zyb）
新闻 内容 ->返回最近新闻（测试）（news）
性别判断 人名字 ->根据人名判断性别（ng）
eat 文字 ->生成表情包
二维码生成 内容 ->生成二维码（qrcode）（仅限英文）
数学题 ->返回数学题""".trimIndent()).recallIn(31000)
                            reply("""更多帮助请发送：
help 翻译
help 图片""".trimMargin()).recallIn(32000)

                             */
                        } else if (ct.size == 2) {
                            when (ct[1]) {
                                "谷歌翻译" -> reply("""支持的翻译语种：
（另：谷歌翻译服务器日常土豆）
简体中文，繁体中文，文言文，粤语，
日语，英语，德语，法语，韩语，芬兰语，犹太语，祖鲁语，南非语，希腊语，
孟加拉语，加泰罗尼亚语，保加利亚语，库尔德语，葡萄牙语，阿拉伯语
象形（阿姆哈拉文）""".trimIndent()).recallIn(30000)

                                "百度翻译" -> reply("""
#支持的语种（即翻译关键字）：
 中文->粤语，粤语->中文（翻译关键字：粤语中文），文言文->中文（翻译关键字：文言文中文），中文->文言文
 韩语，葡萄牙语，阿拉伯语，荷兰语，英语，日语，德语，保加利亚语，希腊语
# 用法：
 翻译 [翻译关键字] [需要翻译的内容]""".trimIndent()).recallIn(30000)
                                "图片" -> reply("""# 用法： 图片 [参数]
目前参数只能为数字（1-9）
不传参则随机
3是宠物，5是明星
其他暂时未知""".trimIndent()).recallIn(30000)
                                "翻译" -> reply("请输入\"help 百度翻译\"或\"help 谷歌翻译\"")
                            }
                        }
                    }
                    "yxpHelp", "yxp帮助", "优学派帮助" -> {
                        reply("""
--优学派方面（快 没 用 了）--
github.com/awesomehhhhh/EbagUtil
yxp照片 uid ->返回uid对应的照片
yxp作业 uid 没写 ->返回uid所有没写作业
yxp答案 uid 学科 第几个 ->返回uid指定学科的没写作业的答案
yxp信息 uid ->返回uid对应信息
yxp积分 uid ->返回uid对应积分
yxp老师评语 uid ->返回uid作业评语""".trimIndent()).recallIn(30000)
                    }
                    "ip" -> command = "python $webapi ip ${ct[1]}"
                    "pos" -> command = "python $webapi pos ${ct[1]}"
                    "qrcode", "二维码生成" -> {
                        type = MessageType.CodeDefineBySelf
                        val qrtext = message.replace("qrcode ", "").replace("二维码生成 ", "")
                        "myqr $qrtext -d \"D:/Program Source/QQBOT/python/Temp\"".execute().waitFor()
                        photopath = "D:/Program Source/QQBOT/python/Temp/qrcode.png"
                        File(photopath).sendAsImage()
                    }
                    "photo", "图片", "每日一图" -> {
                        type = MessageType.CodeDefineBySelf
                        val index: Int = when {
                            ct.size == 1 -> -1
                            ct[1].length >= 2 -> {
                                reply("数字过大，仅支持1-9（包括1-9）")
                                return@subscribeAlways
                            }
                            else -> {
                                try {
                                    ct[1].toInt()
                                } catch (e: NumberFormatException) {
                                    reply("参数不是数字")
                                    return@subscribeAlways
                                }
                            }
                        }
                        val f = "python $webapi photo $index".runExecute().split("|")
                        try {
                            reply(f[1].replace("_", "\n"))
                            File(f[0]).sendAsImage()
                        } catch (e: IndexOutOfBoundsException) {
                            reply("你真倒霉")
                        }
                    }
                    "性别判断", "ng", "Sex" -> command = "python $func ng ${ct[1]}"
                    "hot", "微博热搜", "wb", "微博" -> {
                        type = MessageType.CodeDefineBySelf
                        reply("python $webapi hot".runExecute()).recallIn(30000)
                    }
                    else -> type = null
                }
                if (command==null) return@subscribeAlways
                when (type) {
                    MessageType.Common -> {
                        reply(command.runExecute())
                        type = MessageType.Common
                    }
                    MessageType.Image -> {
                        command.execute().waitFor()
                        File(photopath).sendAsImage()
                        type = MessageType.Common
                    }
                }
            }
        } catch (e: Exception) {
            reply(e.toString())
            e.printStackTrace()
        }
    }

    miraiBot.join() // 等待 机器人 离线, 避免主线程退出
}

suspend fun check(event: MessageEvent): Boolean {
    val message = event.message.content
    if (message.length < 50) return true
    if (message.contains("<?xml version='1.0' encoding='UTF-8' standalone='yes'?>")) return true
    if (event.sender.id == 2854196310L) return true
    if ((event.sender as Member).permission.level == 1) return true
    if (message.contains("bilibili.com")) return true
    if (message.contains("docs.microsoft.com")) return true
    if (message.contains("unity.cn")) return true
    if (message.contains("unity.com")) return true
    if (message.contains("csdn.com")) return true
    if (message.contains("github.com")) return true
    val result = "python $webapi check \"${event.message.content}\"".runExecute()
    if (event.message.content.contains("感兴趣的可以加一下进去交流学习哦")) checkFailed(event, result)
    return if (result.contains("通过")) {
        print(result)
        true
    } else {
        checkFailed(event, result)
        false
    }
}

suspend fun checkFailed(event: MessageEvent, result: String): Int {
    try {
        //(event.sender as Member).kick("Bot测试")
    } catch (err: PermissionDeniedException) {
        event.reply(At(event.sender as Member) + "有违禁信息但权限原因无法踢走\n原因：$result")
    } finally {
        event.reply(At(event.sender as Member) + "有违禁信息\n原因：$result")
    }
    File(elog).writeText(File(elog).readText() + "\n" + event.senderName + " " + event.message.content)
    return when(5){2->3;5->6;else->7}
}

fun String.execute(): Process {
    val runtime = Runtime.getRuntime()
    return runtime.exec(this)
}

fun Process.waitForThis(): Process {
    this.waitFor()
    return this
}

fun String.runExecute(): String = this.execute().waitForThis().inputStream.readString()

fun InputStream.readString(): String {
    val bos = ByteArrayOutputStream()
    return try {
        val a = ByteArray(1)
        var len: Int
        do {
            len = this.read(a)
            bos.write(a)
        } while (-1 != len)
        bos.toString("gbk").dropLast(1)
    } catch (e: Exception) {
        e.printStackTrace()
        e.toString()
    } finally {
        bos.close()
    }
}
