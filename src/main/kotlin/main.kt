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
    val image="\"d:/Program Source/QQBOT/python/image.py\""
    val temp="D:/Program Source/QQBOT/python/Temp/temp.txt"
    val imageTemp="D:/Program Source/QQBOT/python/Temp/temp.jpg"
    val imagePublic="D:/Program Source/QQBOT/python/Temp/FacePublic.jpg"
    val imagePrivate="D:/Program Source/QQBOT/python/Temp/FacePrivate.jpg"

    miraiBot.subscribeAlways<GroupMessageEvent> { event ->
        val message=event.message.content
        val ct=message.split(" ")
        when(ct[0]){
            "yxpLt","yxp老师评语"->{
                val command="python $program yxpLt ${ct[1]} ${ct[2]}"
                val out=command.execute()
                out.waitFor()
                reply(File(temp).readText())
            }
            "yxpPRs","yxpPrs","yxp批改成绩","yxpprs"->{
                val command="python $program yxpRs ${ct[1]} ${ct[2]}"
                val out=command.execute()
                out.waitFor()
                reply(File(temp).readText()) }

            "yxpAs","yxp答案"->{
                val command="python $program yxpAs ${ct[1]} ${ct[2]}${ct[3]}"
                println(command)
                val out=command.execute()
                out.waitFor()
                reply(File(temp).readText()) }
            "yxpPic","yxppic","yxp照片"->{
                val command="python $program yxpPic ${ct[1]}"
                val out=command.execute()
                out.waitFor()
                val file=File(temp)
                if (file.readText()==""){
                    reply("用户不存在")
                    println("ct[0]")
                }
                else{
                    val str="这是 优学派用户 e${ct[1].toInt()}（${file.readText()}） 的头像"
                    reply(str)

                    File(imagePublic).sendAsImageTo(subject)
                    try{
                        File(imagePrivate).sendAsImageTo(subject)}
                    catch(e:Exception){
                        reply("没有设置个人头像，没品位")
                    }
                    println(ct[0])
                }
            }
            "yxpHW","yxp作业","yxpHw","yxp作业完成"->{
                if(ct.size==3){
                    when (ct[2]){
                        "语文","数学","英语","历史","道法","生物","地理","信息","物理","体育","美术","音乐"->{
                            val command="python $program yxpHw ${ct[1]} ${ct[2]}"
                            val out=command.execute()
                            out.waitFor()
                            val file=File(temp)
                            reply(file.readText())
                        }
                        else->{reply("科目不对，仅支持：语文，数学，英语，历史，道法，生物，地理，信息，物理，体育，美术，音乐")}
                    }

                }
                else{
                    reply("给的东西不够或者多了，例子：yxp作业 1585745 生物")
                }
            }
            "yxprd","yxp随机","yxpRand","yxp随机作业"->{
                val command="python $program yxpDCom ${ct[1]}"
                val out=command.execute()
                out.waitFor()
                val file=File(temp)
                reply(file.readText()) }
            "eat"->{
                val command="python $image yz ${ct[1]}"
                val out=command.execute()
                out.waitFor()
                val file=File(imageTemp)
                file.sendAsImageTo(subject) }
            "ip"->{
                val command="python $program ip ${ct[1]}"
                val out = command.execute()
                out.waitFor()
                val file=File(temp)
                reply(file.readText()) }
            "pos"->{
                val command="python $program pos ${ct[1]}"
                val out = command.execute()
                out.waitFor()
                val file=File(temp)
                reply(file.readText())}
            "resend"->{
                when (ct[1]){
                    "text"->{
                        try {
                            val temp="D:/Program Source/QQBOT/python/Temp/temp.txt"
                            val file=File(temp)
                            reply(file.readText())
                        }
                        catch(e:Exception) {
                            reply(e.toString())
                        }
                    }
                    "image"->{
                        try {
                            val temp="D:/Program Source/QQBOT/python/Temp/temp.jpg"
                            val file=File(temp).sendAsImageTo(subject)
                        }
                        catch(e:Exception) {
                            reply(e.toString())
                        }
                    }
                }
            }
        }
    }
    miraiBot.join() // 等待 Bot 离线, 避免主线程退出
}
fun String.execute(): Process {
    val runtime = Runtime.getRuntime()
    return runtime.exec(this)
}
