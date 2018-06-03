package rzaevali.unit

import com.google.gson.GsonBuilder
import org.junit.Assert.assertTrue
import org.junit.Test
import rzaevali.exceptions.UnknownValueException
import rzaevali.utils.extractSchedule
import rzaevali.utils.getSchedule
import java.io.FileReader
import java.nio.file.Files
import java.nio.file.Paths

class ScheduleTest {

    @Test
    fun testParsing() {
        val gson = GsonBuilder().create()

        val groupIds = listOf(7795, 7794, 8891, 8969)

        for (groupId in groupIds) {
            val pdfPath = "src/test/resources/pdf/${groupId}_1_18122017_31122017.pdf"
            val jsonPath = "src/test/resources/json/${groupId}_1_18122017_31122017.json"

            val actualData = extractSchedule(Files.newInputStream(Paths.get(pdfPath)))
            val expectedData = gson.fromJson(FileReader(jsonPath), Map::class.java)["weeks"] as List<*>

            assertTrue("Fail while parsing schedule: $groupId", expectedData == actualData)
        }
    }

    @Test(expected = UnknownValueException::class)
    fun testArgumentChecks() {
        getSchedule(TEST_GROUP_ID, INCORRECT_SEASON)
    }

    companion object {

        private val INCORRECT_SEASON = "null"

        private val TEST_GROUP_ID = "7795"

    }

}
