package rzaevali

import org.junit.Test
import rzaevali.exceptions.UnknownValueException

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import rzaevali.dao.GroupsInfoDao
import rzaevali.dao.ScheduleInfoDao
import rzaevali.utils.*

class DBUtilsTest {

    @Test
    fun testCachedSchedule() {
        assertNull(ScheduleInfoDao.findByGroupIdAndSeason(INCORRECT_GROUP_ID, SEASON_AUTUMN))
        assertNull(ScheduleInfoDao.findByGroupIdAndSeason(INCORRECT_GROUP_ID, SEASON_SPRING))
    }

    @Test
    fun testExistentGroupId() {
        val groupName = GroupsInfoDao.findByGroupId(TEST_GROUP_ID).group
        assertEquals(groupName, TEST_GROUP_NAME)
    }

    @Test(expected = UnknownValueException::class)
    fun testNonExistentGroupId() {
        GroupsInfoDao.findByGroupId(INCORRECT_GROUP_ID)
    }

    companion object {

        private val INCORRECT_GROUP_ID = "null"

        private val INCORRECT_SEASON = "null"

        private val TEST_GROUP_ID = "0000"

        private val TEST_GROUP_NAME = "Test"

    }

}
