package rzaevali

import com.google.common.collect.ImmutableList
import com.google.gson.GsonBuilder
import org.junit.Assert.assertEquals
import org.junit.Test
import rzaevali.exceptions.UnknownValueException
import rzaevali.exceptions.VyatsuScheduleException
import rzaevali.utils.extractSchedule
import rzaevali.utils.getSchedule
import java.io.FileReader
import java.io.IOException
import java.nio.file.Files
import java.nio.file.Paths

class ScheduleTest {

    @Test
    @Throws(IOException::class, VyatsuScheduleException::class)
    fun testParsing() {
        val gson = GsonBuilder().create()

        val groupIds = ImmutableList.of(
                7795, 7794, 8891, 8969
        )

        val pathPattern = "src/test/resources/%s/%s_1_18122017_31122017.%s"

        for (groupId in groupIds) {
            val pdfPath = String.format(pathPattern, "pdf", groupId, "pdf")
            val jsonPath = String.format(pathPattern, "json", groupId, "json")

            val data = extractSchedule(Files.newInputStream(Paths.get(pdfPath)))
            val originalData = gson.fromJson(FileReader(jsonPath), Map::class.java)["weeks"] as List<*>

            assertEquals(Integer.toString(groupId!!), originalData, data)
        }
    }

    @Test(expected = UnknownValueException::class)
    @Throws(VyatsuScheduleException::class)
    fun testArgumentChecks() {
        getSchedule(TEST_GROUP_ID, INCORRECT_SEASON)
    }

    companion object {

        private val INCORRECT_SEASON = "null"

        private val TEST_GROUP_ID = "0000"

    }

}
