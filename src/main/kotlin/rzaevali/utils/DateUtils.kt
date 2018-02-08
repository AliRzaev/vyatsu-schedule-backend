package rzaevali.utils

import java.time.LocalDate
import java.time.Month

fun isAutumn(currentDate: LocalDate): Boolean {
    val monthValue = currentDate.monthValue
    val augustValue = Month.AUGUST.value
    val decemberValue = Month.DECEMBER.value

    return monthValue in augustValue..decemberValue
}

fun isSpring(currentDate: LocalDate): Boolean {
    return !isAutumn(currentDate)
}

fun LocalDate.asString(): String {
    return String.format("%02d%02d%04d", this.dayOfMonth, this.monthValue, this.year)
}

fun String.toLocalDate(): LocalDate {
    val day = Integer.parseInt(this.substring(0, 2))
    val month = Integer.parseInt(this.substring(2, 4))
    val year = Integer.parseInt(this.substring(4))

    return LocalDate.of(year, month, day)
}

fun compareDates(first: List<String>, second: List<String>): Int {
    val firstDate = first[0].toLocalDate()
    val secondDate = second[0].toLocalDate()

    return firstDate.compareTo(secondDate)
}