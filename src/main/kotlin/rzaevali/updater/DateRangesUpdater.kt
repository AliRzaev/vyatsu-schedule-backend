@file:JvmName("DateRangesUpdater")

package rzaevali.updater

import com.mashape.unirest.http.Unirest
import com.mashape.unirest.http.exceptions.UnirestException
import rzaevali.dao.DateRangesDao
import rzaevali.exceptions.UnknownValueException

import java.time.DayOfWeek
import java.time.LocalDate
import java.time.ZoneId

import rzaevali.utils.*
import java.util.HashMap
import java.util.regex.Pattern

@Throws(UnknownValueException::class)
fun main(args: Array<String>) {
    val currentDate = LocalDate.now(ZoneId.of("Europe/Moscow"))
    val currentDay = currentDate.dayOfWeek

    println("Updating")

    if (currentDay != DayOfWeek.SATURDAY) {
        return
    }

    if (isAutumn(currentDate)) {
        updateDateRanges(SEASON_AUTUMN)
    }
    if (isSpring(currentDate)) {
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