package rzaevali.integration

import com.google.gson.GsonBuilder
import com.mashape.unirest.http.Unirest
import org.junit.Test
import java.io.File

class AllGroupsIT {

    private val url = "https://vsuscheduleapi-dev.herokuapp.com"

    private val gson = GsonBuilder().create()

    @Test
    fun testAll() {
        val groups = gson.fromJson(File("src/test/resources/groups.json").reader(), Map::class.java)
        val errors = emptySet<String>()

        groups.forEach {
            val res = Unirest.get("$url/vyatsu/schedule/${it.value}/spring").asString()
            if (res.status != 200) {
                val body = gson.fromJson(res.body, Map::class.java)
                println("error: ${body["error"]}")
                errors.plus(it.value.toString())
            }
        }
    }
}