package rzaevali.routes

import org.apache.logging.log4j.LogManager
import spark.Spark.get
import spark.Spark.path
import java.io.File


private val logger = LogManager.getLogger("vyatsu/v2")

fun vyatsuV2Routes() {
    path("/vyatsu/v2") {
        get("/calls") { _, res ->
            logger.info("/calls")

            res.type("application/json")
            File("src/main/webapp/data/calls-v2.json").readText()
        }

        get("/groups.json") { _, res ->
            logger.info("/groups.json")

            res.type("application/json")
            File("src/main/webapp/data/groups-v2.json").readText()
        }
    }
}

