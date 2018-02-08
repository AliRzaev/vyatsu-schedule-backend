package rzaevali

import org.junit.Test
import rzaevali.exceptions.UnknownValueException

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import rzaevali.utils.*

class DBUtilsTest {

    @Test(expected = UnknownValueException::class)
    @Throws(UnknownValueException::class)
    fun testArgumentChecks1() {
        getCachedSchedule(TEST_GROUP_ID, INCORRECT_SEASON)
    }

    @Test(expected = UnknownValueException::class)
    @Throws(UnknownValueException::class)
    fun testArgumentChecks2() {
        updateDateRanges(INCORRECT_SEASON)
    }

    @Test
    @Throws(UnknownValueException::class)
    fun testCachedSchedule() {
        assertNull(getCachedSchedule(INCORRECT_GROUP_ID, SEASON_AUTUMN))
        assertNull(getCachedSchedule(INCORRECT_GROUP_ID, SEASON_SPRING))
    }

    @Test
    @Throws(UnknownValueException::class)
    fun testExistentGroupId() {
        val groupName = getGroupName(TEST_GROUP_ID)
        assertEquals(groupName, TEST_GROUP_NAME)
    }

    @Test(expected = UnknownValueException::class)
    @Throws(UnknownValueException::class)
    fun testNonExistentGroupId() {
        getGroupName(INCORRECT_GROUP_ID)
    }

    companion object {

        private val INCORRECT_GROUP_ID = "null"

        private val INCORRECT_SEASON = "null"

        private val TEST_GROUP_ID = "0000"

        private val TEST_GROUP_NAME = "Test"

    }

}
