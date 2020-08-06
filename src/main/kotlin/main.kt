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


//@InternalAPI
@InternalCoroutinesApi
suspend fun main() {

    val qqId = 924410958L//Bot的QQ号，需为Long类型，在结尾处添加大写L
    val password = "070304syz"//Bot的密码
    val miraiBot = Bot(qqId, password){
        fileBasedDeviceInfo("device.json")
    }.alsoLogin()//新建Bot并登录
    /*
    miraiBot.subscribeMessages {
        "你好" reply "你好!"
        case("at me") {
            reply(At(sender as Member) + " 给爷爬 ")
        }

        (contains("舔") or contains("刘老板")) {
            reply("刘老板太强了")
        }
    }*/
    val program="\"d:/Program Source/QQBOT/python/websocket.py\""
    val image="\"d:/Program Source/QQBOT/python/image.py\""
    val temp="D:/Program Source/QQBOT/python/Temp/temp.txt"
    val imageTemp="D:/Program Source/QQBOT/python/Temp/temp.jpg"
    val imagePublic="D:/Program Source/QQBOT/python/Temp/FacePublic.jpg"
    val imagePrivate="D:/Program Source/QQBOT/python/Temp/FacePrivate.jpg"
    miraiBot.subscribeAlways<GroupMessageEvent> { event ->
        val message=event.message.content
        val ct=message.split(" ")
        when(ct[0]){
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
            "yxpHW","yxp作业","yxpHw"->{
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
            "yxprd","yxp随机","yxpRand"->{
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
        if(event.message.content.startsWith("resend "))
        {

        }
    }
    miraiBot.join() // 等待 Bot 离线, 避免主线程退出
}
fun String.execute(): Process {
    val runtime = Runtime.getRuntime()
    return runtime.exec(this)
}