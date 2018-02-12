package rzaevali.integration

import com.beust.klaxon.Klaxon
import com.google.gson.GsonBuilder
import com.mashape.unirest.http.Unirest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import rzaevali.utils.SEASON_SPRING

class ApiV1IT {

    companion object {

        private val INCORRECT_GROUP_ID = "null"

        private val INCORRECT_SEASON = "null"

        private val TEST_GROUP_ID = "7795"

        private val TEST_GROUP_NAME = "ИВТб-3302-02-00"

    }

    private val url = "https://vsuscheduleapi-dev.herokuapp.com"

    private val gson = GsonBuilder().create()

    data class ErrorResponse(val error: String)

    @Test
    fun testCalls() {
        val response = Unirest.get("$url/vyatsu/calls").asString()
        assertEquals("Status code must be 200", 200, response.status)
    }

    @Test
    fun testScheduleWithValidInput() {
        val response = Unirest.get("$url/vyatsu/schedule/$TEST_GROUP_ID/$SEASON_SPRING").asString()
        assertEquals("Status code must be 200", 200, response.status)

        val body = gson.fromJson(response.body, Map::class.java)
        assertTrue("No field 'group'", "group" in body)
        assertTrue("No field 'weeks'", "weeks" in body)
        assertTrue("No field 'date_range'", "date_range" in body)

        assertEquals("Invalid group name", TEST_GROUP_NAME, body["group"])
    }

    @Test
    fun testScheduleWithInvalidGroupId() {
        val response = Unirest.get("$url/vyatsu/schedule/$INCORRECT_GROUP_ID/$SEASON_SPRING").asString()
        assertEquals("Status code must be 422", 422, response.status)

        val body = gson.fromJson(response.body, Map::class.java)
        assertTrue("No field 'error'", "error" in body)
    }

    @Test
    fun testScheduleWithInvalidSeason() {
        val response = Unirest.get("$url/vyatsu/schedule/$TEST_GROUP_NAME/$INCORRECT_SEASON").asString()
        assertEquals("Status code must be 422", 422, response.status)

        val body = Klaxon().parse<ErrorResponse>(response.body)
        assertTrue("Invalid structure of response", body != null)
    }

}