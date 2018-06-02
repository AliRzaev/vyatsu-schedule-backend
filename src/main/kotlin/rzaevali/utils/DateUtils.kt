package rzaevali.utils

import java.time.LocalDate
import java.time.Month

/**
 * Determine whether given date belongs to the first season or not.
 * The first season is defined as date interval from August to December
 *
 * @param currentDate date for testing
 * @return true if given date belongs to the first semester, false otherwise
 */
fun isAutumn(currentDate: LocalDate): Boolean {
    val monthValue = currentDate.monthValue
    val augustValue = Month.AUGUST.value
    val decemberValue = Month.DECEMBER.value

    return monthValue in augustValue..decemberValue
}

/**
 * Determine whether given date belongs to the second season or not.
 * The second season is defined as date interval from January to July
 *
 * @param currentDate date for testing
 * @return true if given date belongs to the second semester, false otherwise
 */
fun isSpring(currentDate: LocalDate): Boolean {
    return !isAutumn(currentDate)
}

/**
 * Convert instance of [LocalDate] to string with format ddMMYYYY
 *
 * @return string representation of [LocalDate] instance
 */
fun LocalDate.asString(): String {
    return String.format("%02d%02d%04d", this.dayOfMonth, this.monthValue, this.year)
}

/**
 * Convert date string with format ddMMYYYY to [LocalDate] instance
 *
 * @return [LocalDate] instance with date from string
 */
fun String.toLocalDate(): LocalDate {
    val day = Integer.parseInt(this.substring(0, 2))
    val month = Integer.parseInt(this.substring(2, 4))
    val year = Integer.parseInt(this.substring(4))

    return LocalDate.of(year, month, day)
}

/**
 * Compare date ranges by its first components
 *
 * @param first first date range
 * @param second second date range
 * @return result of comparison of first components by [LocalDate.compareTo] method
 */
fun compareDates(first: List<String>, second: List<String>): Int {
    val firstDate = first[0].toLocalDate()
    val secondDate = second[0].toLocalDate()

    return firstDate.compareTo(secondDate)
}