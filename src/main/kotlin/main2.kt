import kotlinx.serialization.*
import kotlinx.serialization.json.Json
import net.mamoe.mirai.BotFactory
import net.mamoe.mirai.alsoLogin
import net.mamoe.mirai.contact.User
import net.mamoe.mirai.contact.getMember
import net.mamoe.mirai.contact.nameCardOrNick
import net.mamoe.mirai.event.events.*
import net.mamoe.mirai.message.data.*
import net.mamoe.mirai.message.data.Image.Key.queryUrl
import net.mamoe.mirai.utils.BotConfiguration
import java.io.ByteArrayOutputStream
import java.io.File
import java.lang.Exception

// Python script path
const val PYTHONSCRIPT_WEBAPI = "D:\\Program Source\\AwesomeCore_git\\webapi.py"

// Analyse key names
const val INTERESTING_KEY = "Such Interesting"
const val INTERESTING_NAME = "真有意思"

suspend fun main() {
    val bot = BotFactory.newBot(924410958, "PASSWORD", BotConfiguration {
        fileBasedDeviceInfo("device.json")
        protocol = BotConfiguration.MiraiProtocol.ANDROID_PHONE
    }).alsoLogin()
    val waitingSystem = MessageWaitingSystem()
    val group = bot.getGroup(715146911L)
    //group?.botAsMember?.nudge()?.sendTo(group)
    //group?.getMember(3168287806L)?.nudge()?.sendTo(group)
    bot.eventChannel.subscribeAlways<GroupMuteAllEvent> { event ->
        if (event.new) {
            println("Receive an new event: GroupMuteAllEvent\n${event.operator?.nameCardOrNick} 解除了全员禁言")
            event.group.sendMessage("Receive an new event: GroupMuteAllEvent\n${event.operator?.nameCardOrNick} 解除了全员禁言")
        }
    }
    bot.eventChannel.subscribeAlways<GroupMessageEvent> { event ->
        waitingSystem.checkWaiting(event)
        if (event.group.id == 963322306L || event.group.id == 715146911L || event.group.id == 311342702L) {
            analyse2105(event)
        }
        when (event.message.content.replace("：", ":")) {
            "AwesomeBot:analyse" -> getAnalyse2105Info(event)
            "AwesomeBot:help" -> getHelpContent(event)
            "AwesomeBot:status" -> getBotStatus(event)
            "AwesomeBot:image" -> imageRecognition(event, waitingSystem)
        }
    }
    bot.eventChannel.subscribeAlways<BotInvitedJoinGroupRequestEvent> { event ->
        event.accept()
    }
}

suspend fun translateWord(event: GroupMessageEvent) {

}

suspend fun getBotStatus(event: GroupMessageEvent) {
    event.subject.sendMessage(
        """
        AwesomeBot (github.com/awesomehhhhh/AwesomeBot) ,最后更新于 2021/09/11 17:06:12
        Created by Awesomehhhhh@3168287806
        Depend on mirai v2.6.4 (github.com/mamoe/mirai)
    """.trimIndent()
    )
}

/**
 * 图片识别
 *
 * 使用了[MessageWaitingSystem]
 */
suspend fun imageRecognition(event: GroupMessageEvent, waitingSystem: MessageWaitingSystem) {
    event.subject.sendMessage("请发送图片以进行图片识别")
    waitingSystem.subscribe(event.sender, MessageWaitingKey(
        { messageChain -> messageChain.contains(Image) },
        { messageEvent, messageWaitingSystem ->
            messageWaitingSystem.unsubscribe(messageEvent.sender)
            messageEvent.subject.sendMessage("未发送图片，图片识别已取消。")
        }) {
        val imageUrl = it.message[Image]?.queryUrl()
        event.subject.sendMessage(
            pythonCommandRun("python \"$PYTHONSCRIPT_WEBAPI\" imageSearch $imageUrl")
        )
    })
}

/**
 * 返回Help帮助文档
 */
suspend fun getHelpContent(event: GroupMessageEvent) {
    event.subject.sendMessage(
        """
        请注意：目前操纵AwesomeBot机器人需要加AwesomeBot:前缀
        
        AwesomeBot:analyse 统计发了多少次统计「$INTERESTING_NAME」
        AwesomeBot:help 显示帮助
        AwesomeBot:status 显示目前机器人状态
        AwesomeBot:image 图片识别
    """.trimIndent()
    )
}

/**
 * 返回在2105班统计的 真有意思 ([INTERESTING_KEY]) 的次数并回复
 */
suspend fun getAnalyse2105Info(event: GroupMessageEvent) {
    var replyResult = "统计谁说了多少次「$INTERESTING_NAME」的数据（并不全）如下：\n*请注意，AwesomeBot离线时无法统计*"
    val file = File("D:\\Program Source\\QQBOT_depend_mirai2\\src\\Analyse2105.json")
    if (!file.exists()) {
        event.subject.sendMessage("暂时没有分析数据")
        return
    }
    val jsonContent = Json.decodeFromString<Analyse2105Database>(file.readText())

    jsonContent.data[INTERESTING_KEY]?.forEach {
        replyResult += "\n${event.group.getMember(it.key)?.nameCardOrNick ?: "@${it.key}"} ： ${it.value} 次"
    }
    event.subject.sendMessage(replyResult)
}

/**
 * 写入2105真有意思数据
 */
fun analyse2105(event: GroupMessageEvent) {
    val qid = event.sender.id
    val file = File("D:\\Program Source\\QQBOT_depend_mirai2\\src\\Analyse2105.json")
    if (!file.exists()) {
        file.createNewFile()
        file.writeText("{\"data\":{\"$INTERESTING_KEY\":{}}}")
    }
    val jsonContent = Json.decodeFromString<Analyse2105Database>(file.readText())
    if (event.message.content.contentEquals(INTERESTING_NAME)) {
        val jsonData = jsonContent.data[INTERESTING_KEY]!!
        jsonData[qid] = jsonData[qid]?.plus(1) ?: 1
        file.writeText(Json.encodeToString(jsonContent))
    }
}

@Serializable
data class Analyse2105Database(@Contextual val data: MutableMap<String, MutableMap<Long, Int>>)

/////////
data class MessageWaitingKey(
    val checkAction: suspend (MessageChain) -> Boolean,
    val failureAction: suspend (MessageEvent, MessageWaitingSystem) -> Unit,
    val callbackAction: suspend (MessageEvent) -> Unit
)

class MessageWaitingSystem {
    private val isWaiting: Boolean
        get() {
            return subscribingList.isNotEmpty()
        }
    private var subscribingList: MutableMap<Long, MessageWaitingKey> = mutableMapOf()

    /**
     * 开始监听事件
     */
    fun subscribe(member: User, messageWaitingKey: MessageWaitingKey) {
        subscribingList[member.id] = messageWaitingKey
    }

    /**
     * 取消监听事件
     */
    fun unsubscribe(member: User) {
        subscribingList.remove(member.id)
    }

    /**
     * 当有新消息时检测所有的监听事件并响应
     */
    suspend fun checkWaiting(event: GroupMessageEvent) {
        if (isWaiting) {
            val waitingKey = subscribingList[event.sender.id]
            val result = waitingKey?.checkAction?.invoke(event.message)
            if (result == true) {
                waitingKey.callbackAction.invoke(event)
                unsubscribe(event.sender)
            } else if (result == false) waitingKey.failureAction.invoke(event, this)
        }
    }
}

/**
 * 在Console中运行Python命令
 * @see Runtime.exec
 */
fun pythonCommandRun(string: String): String {
    println("Run: $string")
    val runtime = Runtime.getRuntime()
    val process = runtime.exec(string)
    process.waitFor()
    val bos = ByteArrayOutputStream()
    return try {
        val a = ByteArray(1)
        var len: Int
        do {
            len = process.inputStream.read(a)
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