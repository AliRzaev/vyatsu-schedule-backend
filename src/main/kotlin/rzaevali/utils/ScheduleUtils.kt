package rzaevali.utils

import rzaevali.dao.DateRangesDao
import rzaevali.dao.GroupsInfoDao
import rzaevali.dao.ScheduleInfoDao
import rzaevali.exceptions.UnknownValueException
import rzaevali.exceptions.VyatsuScheduleException

private const val BASE_URL = "https://www.vyatsu.ru/reports/schedule/Group/%s_%s_%s_%s.pdf"

private val SCHEDULE_CACHE_ENABLED = (System.getenv("SCHEDULE_CACHE") ?: "disabled") == "enabled"

/**
 * Schedule of group.
 *
 * This class contains information about schedule of some group
 *
 * @param weeks schedule as three-dimension array: the week, the day, the lesson
 * @param group name of group
 * @param date_range two-weeks range of schedule
 */
data class Schedule(val weeks: NestedList, val group: String, val date_range: List<String>)

/**
 * Fetch schedule of some group by its id and season name.
 * Schedule can be either fetched from cache or indirectly from site.
 *
 * @param groupId group id
 * @param season season name
 * @return instance of [Schedule] containing schedule of group
 * @throws VyatsuScheduleException if some errors occurred during fetching of schedule
 */
@Throws(VyatsuScheduleException::class)
fun getSchedule(groupId: String, season: String): Schedule {
    checkSeason(season)

    return if (SCHEDULE_CACHE_ENABLED) {
        getScheduleUsingCache(groupId, season)
    } else {
        getScheduleFromSite(groupId, season)
    }
}

/**
 * Fetch schedule of some group indirectly from site
 *
 * @param groupId group id
 * @param season season name
 * @return instance of [Schedule] containing schedule of group
 * @throws VyatsuScheduleException if some errors occurred during fetching of schedule
 */
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

/**
 * Fetch schedule of some from cache.
 * If schedule in cache is out of date then schedule will be fetched indirectly from site.
 *
 * @param groupId group id
 * @param season season name
 * @return instance of [Schedule] containing schedule of group
 * @throws VyatsuScheduleException if some errors occurred during fetching of schedule
 */
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

/**
 * Build URL of the pdf document with schedule by group id, season and date range
 *
 * @param groupId group id
 * @param season season name
 * @param range date range specifying two-weeks range of schedule
 * @throws UnknownValueException if season name isn't valid
 */
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