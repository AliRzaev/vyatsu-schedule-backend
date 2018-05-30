import org.litote.kmongo.getCollection
import rzaevali.utils.getDatabase
import java.util.*

data class LogsInfo(val groupId: String, val season: String, val date: Date)

object LogsDao {

    private const val LOGS_COLLECTION = "logs"

    fun insertOneLogRequest(groupId: String, season: String) {
        val collection = getDatabase()
                .getCollection<LogsInfo>(LOGS_COLLECTION)

        val date: Date = GregorianCalendar.getInstance(TimeZone.getTimeZone("Europe/Moscow")).time
        val document = LogsInfo(groupId, season, date)

        collection.insertOne(document)
    }

}