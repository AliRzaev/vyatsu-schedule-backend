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

            res.redirect("/static/v2/calls.json")
        }

        get("/groups.json") { _, res ->
            logger.info("/groups.json")

            res.redirect("/static/v2/groups.json")
        }
    }
}

