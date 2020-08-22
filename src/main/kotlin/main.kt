import net.mamoe.mirai.Bot
import net.mamoe.mirai.alsoLogin
import net.mamoe.mirai.event.*
import net.mamoe.mirai.join
import net.mamoe.mirai.message.*
import net.mamoe.mirai.message.data.*
import kotlinx.coroutines.InternalCoroutinesApi
import net.mamoe.mirai.message.code.parseMiraiCode
import java.io.File
import java.lang.Exception


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
    val imagePhoto="D:/Program Source/QQBOT/python/Temp/photo.png"
    val imagePrivate="D:/Program Source/QQBOT/python/Temp/FacePrivate.jpg"

    miraiBot.subscribeAlways<GroupMessageEvent> { event ->
        try{
            val message = event.message.content
            val n = event.message[Image]
            val ct = message.split(" ")
            when (ct[0]) {
                "yxpLt", "yxp老师评语" -> {
                    val command = "python $program yxpLt ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
                    reply(File(temp).readText())
                }
                "数学题", "math" -> {
                    val command = "python $webapi math"
                    val out = command.execute()
                    out.waitFor()
                    File(imageMath).sendAsImage()
                }
                "yxpInfo", "yxp信息" -> {
                    val command = "python $program yxpInfo ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
                    reply(File(temp).readText())
                }
                "yxpNm", "yxp积分" -> {
                    val command = "python $program yxpNm ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
                    reply(File(temp).readText())
                }
                "yxpPRs", "yxpPrs", "yxp批改成绩", "yxpRs" -> {
                    val command = "python $program yxpRs ${ct[1]} ${ct[2]}"
                    val out = command.execute()
                    out.waitFor()
                    reply(File(temp).readText())
                }

                "yxpAs", "yxp答案" -> {
                    val command = "python $program yxpAs ${ct[1]} ${ct[2]}${ct[3]}"
                    println(command)
                    val out = command.execute()
                    out.waitFor()
                    reply(File(temp).readText())
                }
                "yxpPic", "yxppic", "yxp照片" -> {
                    val command = "python $program yxpPic ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
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
                                val command = "python $program yxpHw ${ct[1]} ${ct[2]}"
                                val out = command.execute()
                                out.waitFor()
                                val file = File(temp)
                                reply(file.readText())
                            }
                            else -> {
                                reply("科目不对，仅支持：语文，数学，英语，历史，道法，生物，地理，信息，物理，体育，美术，音乐")
                            }
                        }

                    } else {
                        reply("给的东西不够或者多了，例子：yxp作业 1585745 生物")
                    }
                }
                "yxprd", "yxp随机", "yxpRand", "yxp随机作业" -> {
                    val command = "python $program yxpDCom ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
                    val file = File(temp)
                    reply(file.readText())
                }
                "eat" -> {
                    val command = "python $image yz ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
                    val file = File(imageTemp)
                    file.sendAsImageTo(subject)
                }
                "trsWd", "翻译单词", "trswd" -> {
                    var engine = ""
                    if (ct.size == 2) {
                        engine = "-"
                    } else {
                        engine = ct[2]
                    }
                    val command = "python $webapi trsWd ${ct[1]} ${engine}"
                    val out = command.execute()
                    out.waitFor()
                    reply(File(temp).readText())
                }
                "trs", "翻译", "translate" -> {
                    var engine = ""
                    var dest = "zh-cn"
                    if (ct.size == 3) {
                        engine = "-"
                    } else {
                        engine = ct[3]
                    }
                    if (ct.size == 2) {
                        engine = "-"
                    } else {
                        dest = ct[2]
                    }
                    val command = "python $webapi trs ${ct[1]} ${dest} ${engine}"
                    val out = command.execute()
                    out.waitFor()
                    reply(File(temp).readText())
                }
                "搜索建议", "idea", "search" -> {
                    val command = "python $webapi search ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
                    val file = File(temp)
                    reply(file.readText())
                }
                "help", "帮助" -> {
                    reply("""->括号内为简写如："搜索建议 机器人"可替换成"idea 机器人"<-
    github.com/awesomehhhhh/ebagqbot
    翻译 需要翻译的文字 翻译的语种 -> 返回翻译结果（trs）
    翻译单词 需要翻译的单词 -> 返回单词英文结果和相关信息（trsWd）
    搜索建议 信息 ->返回搜索建议（idea）
    帮助 ->返回帮助（help）
    性别判断 人名字 ->根据人名判断性别（ng）
    eat 文字 ->生成表情包
    二维码生成 内容 ->生成二维码（qrcode）（仅限英文）
    数学题 ->返回数学题""".trimIndent())
                }
                "yxpHelp", "yxp帮助" -> {
                    reply("""
    --------------------优学派方面（快 没 用 了）
    yxp照片 uid ->返回uid对应的照片
    yxp作业 uid 没写 ->返回uid所有没写作业
    yxp答案 uid 学科 第几个 ->返回uid指定学科的没写作业的答案
    yxp信息 uid ->返回uid对应信息
    yxp积分 uid ->返回uid对应积分
    yxp老师评语 uid ->返回uid作业评语""".trimIndent())
                }
                "ip" -> {
                    val command = "python $webapi ip ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
                    val file = File(temp)
                    reply(file.readText())
                }
                "pos" -> {
                    val command = "python $webapi pos ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
                    val file = File(temp)
                    reply(file.readText())
                }
                "qrcode", "二维码生成" -> {
                    val qrtext = message.replace("qrcode", "").replace("二维码生成","")
                    val command = "myqr ${qrtext} -d \"D:/Program Source/QQBOT/python/Temp\""
                    println(command)
                    val out = command.execute()
                    out.waitFor()
                    File("D:/Program Source/QQBOT/python/Temp/qrcode.png").sendAsImage()
                }
                "photo","图片","每日一图"->{
                    val command = "python $webapi photo"
                    val out = command.execute()
                    out.waitFor()
                    File(imagePhoto).sendAsImage()
                    reply(File(temp).readText())
                }
                "性别判断", "ng", "Sex" -> {
                    val command = "python $func ng ${ct[1]}"
                    val out = command.execute()
                    out.waitFor()
                    reply(File(temp).readText())
                }
                "resend" -> {
                    when (ct[1]) {
                        "text" -> {
                            try {
                                val temp = "D:/Program Source/QQBOT/python/Temp/temp.txt"
                                val file = File(temp)
                                reply(file.readText())
                            } catch (e: Exception) {
                                reply(e.toString())
                            }
                        }
                        "image" -> {
                            try {
                                val temp = "D:/Program Source/QQBOT/python/Temp/temp.jpg"
                                val file = File(temp).sendAsImageTo(subject)
                            } catch (e: Exception) {
                                reply(e.toString())
                            }
                        }
                    }
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
