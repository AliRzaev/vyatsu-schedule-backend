package rzaevali.routes

import org.apache.logging.log4j.LogManager
import spark.Spark.get
import spark.Spark.path

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

        get("/groups/by_faculty.json") {_, res ->
            logger.info("/groups/by_faculty.json")

            res.redirect("/static/v2/groups/by_faculty.json")
        }
    }
}

