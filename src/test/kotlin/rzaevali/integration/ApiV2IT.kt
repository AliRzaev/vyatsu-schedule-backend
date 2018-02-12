package rzaevali.integration

import com.beust.klaxon.Klaxon
import com.mashape.unirest.http.Unirest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test


class ApiV2IT {
    private val url = "https://vsuscheduleapi-dev.herokuapp.com"

    data class Calls(val start: String, val end: String)

    @Test
    fun testCalls() {
        val response = Unirest.get("$url/vyatsu/v2/calls").asString()
        assertEquals("Status code must be 200", 200, response.status)

        val body = Klaxon().parseArray<Calls>(response.body)
        assertTrue("Invalid structure of response", body != null)
        assertEquals("The count of lessons doesn't equal to 7", 7, body?.size)
    }
}