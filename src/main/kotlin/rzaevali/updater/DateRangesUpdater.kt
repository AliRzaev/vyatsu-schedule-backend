@file:JvmName("DateRangesUpdater")

package rzaevali.updater

import com.mashape.unirest.http.Unirest
import com.mashape.unirest.http.exceptions.UnirestException
import rzaevali.dao.DateRangesDao
import rzaevali.exceptions.UnknownValueException
import rzaevali.utils.*
import java.time.DayOfWeek
import java.time.LocalDate
import java.time.ZoneId
import java.util.*

@Throws(UnknownValueException::class)
fun main(args: Array<String>) {
    val currentDate = LocalDate.now(ZoneId.of("Europe/Moscow"))
    val currentDay = currentDate.dayOfWeek
    val forced = "--forced" in args

    println("Updating")

    if (currentDay != DayOfWeek.SATURDAY && !forced) {
        return
    }

    if (isAutumn(currentDate) || !forced) {
        updateDateRanges(SEASON_AUTUMN)
    }
    if (isSpring(currentDate) || !forced) {
        updateDateRanges(SEASON_SPRING)
    }
}

private const val GROUPS_LIST_URL =
        "https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html"

@Throws(UnknownValueException::class)
private fun updateDateRanges(season: String) {
    try {
        getRangesFromSite(season).forEach({ groupId, range ->
            DateRangesDao.insertOneOrUpdate(groupId, season, range)
        })
    } catch (e: UnirestException) {
        e.printStackTrace()
    }
}

@Throws(UnirestException::class, UnknownValueException::class)
private fun getRangesFromSite(season: String): Map<String, Pair<String, String>> {
    val seasonKey = getSeasonKey(season)
    val html = Unirest.get(GROUPS_LIST_URL).asString().body
    val regex = Regex("""/reports/schedule/Group/(\d{4})_${seasonKey}_(\d{8})_(\d{8})\.pdf""")

    val dateRanges = HashMap<String, Pair<LocalDate, LocalDate>>()
    regex.findAll(html).forEach { result ->
        val (groupId, first, second) = result.destructured

        val newRange = Pair(first.toLocalDate(), second.toLocalDate())
        val oldRange = dateRanges[groupId]

        if (oldRange == null || oldRange.first < newRange.first) {
            dateRanges[groupId] = newRange
        }
    }

    return dateRanges.mapValues {
        Pair(it.value.first.asString(), it.value.second.asString())
    }
}