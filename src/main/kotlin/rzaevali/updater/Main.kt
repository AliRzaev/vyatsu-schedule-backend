@file:JvmName("Main")

package rzaevali.updater

import rzaevali.exceptions.UnknownValueException
import rzaevali.utils.DateUtils

import java.time.DayOfWeek
import java.time.LocalDate
import java.time.ZoneId

import rzaevali.utils.*

@Throws(UnknownValueException::class)
fun main(args: Array<String>) {
    val currentDate = LocalDate.now(ZoneId.of("Europe/Moscow"))
    val currentDay = currentDate.dayOfWeek

    println("Updating")

    if (currentDay != DayOfWeek.SATURDAY) {
        return
    }

    if (DateUtils.isAutumn(currentDate)) {
        updateDateRanges(SEASON_AUTUMN)
    }
    if (DateUtils.isSpring(currentDate)) {
        updateDateRanges(SEASON_SPRING)
    }
}
