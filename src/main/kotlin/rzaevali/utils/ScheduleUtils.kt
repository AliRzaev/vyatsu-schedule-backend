package rzaevali.utils

import rzaevali.dao.DateRangesDao
import rzaevali.dao.GroupsInfoDao
import rzaevali.dao.ScheduleInfoDao
import rzaevali.exceptions.UnknownValueException
import rzaevali.exceptions.VyatsuScheduleException

private const val BASE_URL = "https://www.vyatsu.ru/reports/schedule/Group/%s_%s_%s_%s.pdf"

private val SCHEDULE_CACHE_ENABLED = (System.getenv("SCHEDULE_CACHE") ?: "disabled") == "enabled"

data class Schedule(val weeks: NestedList, val group: String, val date_range: List<String>)

@Throws(VyatsuScheduleException::class)
fun getSchedule(groupId: String, season: String): Schedule {
    checkSeason(season)

    return if (SCHEDULE_CACHE_ENABLED) {
        getScheduleUsingCache(groupId, season)
    } else {
        getScheduleFromSite(groupId, season)
    }
}

@Throws(VyatsuScheduleException::class)
private fun getScheduleFromSite(groupId: String, season: String): Schedule {
    val range = DateRangesDao.findByGroupIdAndSeason(groupId, season).range
    val group = GroupsInfoDao.findByGroupId(groupId).group
    val url = buildUrl(groupId, season, range)

    return Schedule(
            extractSchedule(url),
            group,
            range
    )
}

@Throws(VyatsuScheduleException::class)
private fun getScheduleUsingCache(groupId: String, season: String): Schedule {
    val range = DateRangesDao.findByGroupIdAndSeason(groupId, season).range
    val group = GroupsInfoDao.findByGroupId(groupId).group
    val url = buildUrl(groupId, season, range)
    val cachedSchedule = ScheduleInfoDao.findByGroupIdAndSeason(groupId, season)

    return if (cachedSchedule == null || compareDates(range, cachedSchedule.range) > 0) {
        val weeks = extractSchedule(url)
        ScheduleInfoDao.insertOneOrUpdate(
                groupId,
                season,
                range,
                weeks
        )

        Schedule(weeks, group, range)
    } else {
        Schedule(cachedSchedule.schedule, group, range)
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