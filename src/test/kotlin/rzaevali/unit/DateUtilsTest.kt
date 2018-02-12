package rzaevali.unit

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import rzaevali.utils.compareDates
import rzaevali.utils.isAutumn
import rzaevali.utils.isSpring
import rzaevali.utils.toLocalDate
import java.time.LocalDate

class DateUtilsTest {

    @Test
    fun testDate() {
        for (month in 1..7) {
            assertTrue(isSpring(LocalDate.of(2017, month, 1)))
        }

        for (month in 8..12) {
            assertTrue(isAutumn(LocalDate.of(2017, month, 1)))
        }
    }

    @Test
    fun testDateComparison() {
        val firstDate = listOf("11102017", "25102017")
        val secondDate = listOf("31102017", "13112017")

        assertTrue(compareDates(firstDate, secondDate) < 1)
    }

    @Test
    fun testDateParsing() {
        val original = LocalDate.of(2018, 1, 2)
        val parsed = "02012018".toLocalDate()

        assertEquals(original, parsed)
    }

}
