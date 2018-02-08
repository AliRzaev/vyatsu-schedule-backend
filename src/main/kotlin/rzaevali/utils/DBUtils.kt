package rzaevali.utils

import com.mashape.unirest.http.Unirest
import com.mashape.unirest.http.exceptions.UnirestException
import com.mongodb.MongoClientURI
import org.litote.kmongo.*
import org.litote.kmongo.MongoOperator.set
import rzaevali.exceptions.UnknownValueException
import java.time.LocalDate
import java.util.*
import java.util.regex.Pattern

private const val DATE_RANGES_COLLECTION = "schedule_ranges"

private const val GROUPS_INFO_COLLECTION = "groups_info"

private const val SCHEDULE_COLLECTION = "schedules"

private const val GROUPS_LIST_URL =
        "https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html"

private val dbUri = MongoClientURI(System.getenv("MONGODB_URI"))

private val dbClient = KMongo.createClient(dbUri)

private val database = dbClient.getDatabase(dbUri.database)

const val SEASON_AUTUMN = "autumn"

const val SEASON_SPRING = "spring"

data class DateRange(val groupId: String, val season: String, val range: List<String>)

data class GroupInfo(val groupId: String, val group: String, val faculty: String)

data class ScheduleInfo(
        val groupId: String,
        val season: String,
        val range: List<String>,
        val schedule: NestedList)

@Throws(UnknownValueException::class)
fun getGroupName(groupId: String): String {
    val collection = database.getCollection<GroupInfo>(GROUPS_INFO_COLLECTION)

    val query = """{
            "groupId": "$groupId"
    }"""

    val res = collection.findOne(query)

    if (res != null) {
        return res.group
    } else {
        throw UnknownValueException("Unknown groupId: $groupId")
    }
}

@Throws(UnknownValueException::class)
fun updateDateRanges(season: String) {
    try {
        val collection = database.getCollection<DateRange>(DATE_RANGES_COLLECTION)

        getRangesFromSite(season).forEach({ groupId, range ->
            val query = """{
                    "groupId": "$groupId",
                    "season":  "$season"
            }"""

            val listRange = range.toList()

            if (collection.findOne(query) != null) {
                val update = """{
                    "$set": {
                        "range": ${listRange.json}
                    }
                }"""

                collection.findOneAndUpdate(query, update)
            } else {
                val entry = DateRange(groupId, season, listRange)
                collection.insertOne(entry)
            }
        })
    } catch (e: UnirestException) {
        e.printStackTrace()
    }
}

@Throws(UnknownValueException::class)
fun getCachedSchedule(groupId: String, season: String): ScheduleInfo? {
    checkSeason(season)

    val collection = database.getCollection<ScheduleInfo>(SCHEDULE_COLLECTION)

    val query = """{
            "groupId": "$groupId",
            "season":  "$season"
    }"""

    return collection.findOne(query)
}

@Throws(UnknownValueException::class)
fun updateSchedule(scheduleInfo: ScheduleInfo) {
    checkSeason(scheduleInfo.season)

    val collection = database.getCollection<ScheduleInfo>(SCHEDULE_COLLECTION)
    val query = """{
            "groupId": "${scheduleInfo.groupId}",
            "season":  "${scheduleInfo.season}"
    }"""

    if (collection.findOne(query) != null) {
        val update = """{
            "$set": {
                "range":    ${scheduleInfo.range.json},
                "schedule": ${scheduleInfo.schedule.json}
            }
        }"""

        collection.findOneAndUpdate(query, update)
    } else {
        collection.insertOne(scheduleInfo)
    }
}

@Throws(UnirestException::class, UnknownValueException::class)
private fun getRangesFromSite(season: String): Map<String, Pair<String, String>> {
    val seasonKey = getSeasonKey(season)
    val html = Unirest.get(GROUPS_LIST_URL).asString().body
    val pattern = Pattern.compile(String.format("/reports/schedule/Group/(\\d{4})_%s_(\\d{8})_(\\d{8})\\.pdf", seasonKey))
    val matcher = pattern.matcher(html)

    val dateRanges = HashMap<String, Pair<LocalDate, LocalDate>>()
    while (matcher.find()) {
        val groupId = matcher.group(1)
        val first = matcher.group(2).toLocalDate()
        val second = matcher.group(3).toLocalDate()

        val newRange = Pair(first, second)
        val oldRange = dateRanges[groupId]

        if (oldRange == null || oldRange.first < newRange.first) {
            dateRanges[groupId] = newRange
        }
    }

    return dateRanges.mapValues {
        Pair(it.value.first.asString(), it.value.second.asString())
    }
}

@Throws(UnknownValueException::class)
private fun checkSeason(season: String): String {
    return if (season != SEASON_AUTUMN && season != SEASON_SPRING) {
        throw UnknownValueException("Unknown season: $season")
    } else {
        season
    }
}

@Throws(UnknownValueException::class)
internal fun getDateRange(groupId: String, season: String): List<String> {
    val collection = database.getCollection<DateRange>(DATE_RANGES_COLLECTION)

    val query = """{
            "groupId": "$groupId",
            "season":  "$season"
    }"""

    val res = collection.findOne(query)

    if (res != null) {
        return res.range
    } else {
        throw UnknownValueException("Unknown groupId: $groupId")
    }
}

@Throws(UnknownValueException::class)
internal fun getSeasonKey(season: String): String {
    checkSeason(season)

    return if (season == SEASON_AUTUMN) "1" else "2"
}