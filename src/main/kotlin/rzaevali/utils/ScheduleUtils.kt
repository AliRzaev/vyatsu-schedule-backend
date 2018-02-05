package rzaevali.utils

import rzaevali.exceptions.UnknownValueException
import rzaevali.exceptions.VyatsuScheduleException

private const val BASE_URL = "https://www.vyatsu.ru/reports/schedule/Group/%s_%s_%s_%s.pdf"

private val SCHEDULE_CACHE_ENABLED = (System.getenv("SCHEDULE_CACHE") ?: "disabled") == "enabled"

data class Schedule(val weeks: NestedList, val group: String, val date_range: List<String>)

fun compareDates(first: List<String>, second: List<String>): Int {
    val firstDate = first[0].toLocalDate()
    val secondDate = second[0].toLocalDate()

    return firstDate.compareTo(secondDate)
}

@Throws(VyatsuScheduleException::class)
fun getSchedule(groupId: String, season: String): Schedule {
    return if (SCHEDULE_CACHE_ENABLED) {
        getScheduleUsingCache(groupId, season)
    } else {
        getScheduleFromSite(groupId, season)
    }
}

@Throws(VyatsuScheduleException::class)
private fun getScheduleFromSite(groupId: String, season: String): Schedule {
    val range = getDateRange(groupId, season)
    val group = getGroupName(groupId)
    val url = buildUrl(groupId, season, range)

    return Schedule(
            extractSchedule(url),
            group,
            range
    )
}

@Throws(VyatsuScheduleException::class)
private fun getScheduleUsingCache(groupId: String, season: String): Schedule {
    val range = getDateRange(groupId, season)
    val group = getGroupName(groupId)
    val url = buildUrl(groupId, season, range)
    val cachedSchedule = getCachedSchedule(groupId, season)

    if (cachedSchedule == null || compareDates(range, cachedSchedule.range) > 0) {
        val weeks = extractSchedule(url)
        updateSchedule(ScheduleInfo(
                groupId,
                season,
                range,
                weeks
        ))

        return Schedule(
                weeks,
                group,
                range
        )
    } else {
        return Schedule(
                cachedSchedule.schedule,
                group,
                range
        )
    }
}

@Throws(UnknownValueException::class)
private fun buildUrl(groupId: String, season: String, range: List<String>): String {
    return String.format(
            BASE_URL,
            groupId,
            getSeasonKey(season),
            range[0],
            range[1]
    )
}