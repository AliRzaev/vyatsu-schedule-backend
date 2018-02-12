package rzaevali.unit

import org.junit.Assert.assertEquals
import org.junit.Test
import rzaevali.utils.SEASON_AUTUMN
import rzaevali.utils.SEASON_SPRING
import rzaevali.utils.checkSeason
import rzaevali.utils.getSeasonKey

class SeasonUtilsTest {

    @Test
    fun testGetSeasonKey() {
        assertEquals("Incorrect season key", "1", getSeasonKey(SEASON_AUTUMN))
        assertEquals("Incorrect season key", "2", getSeasonKey(SEASON_SPRING))
    }

    @Test
    fun checkSeason() {
        assertEquals("Season checking failed", SEASON_AUTUMN, checkSeason(SEASON_AUTUMN))
        assertEquals("Season checking failed", SEASON_SPRING, checkSeason(SEASON_SPRING))
    }

}