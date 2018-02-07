package rzaevali.routes

import org.apache.logging.log4j.LogManager
import org.litote.kmongo.json
import rzaevali.exceptions.VyatsuScheduleException
import rzaevali.utils.getSchedule
import spark.Spark.get
import spark.Spark.path
import java.io.File


private val logger = LogManager.getLogger("vyatsu")

fun vyatsuRoutes() {
    path("/vyatsu") {
        get("/calls") { _, res ->
            logger.info("/calls")

            res.type("application/json")
            File("src/main/webapp/data/calls.json").readText()
        }

        get("/groups.json") { _, res ->
            logger.info("/groups.json")

            res.type("application/json")
            File("src/main/webapp/data/groups.json").readText()
        }

        get("/groups.xml") { _, res ->
            logger.info("/groups.xml")

            res.type("application/xml")
            File("src/main/webapp/data/groups.xml").readText()
        }

        get("/groups/by_faculty.json") { _, res ->
            logger.info("/groups/by_faculty.json")

            res.type("application/json")
            File("src/main/webapp/data/faculties.json").readText()
        }

        get("/groups/by_faculty.xml") { _, res ->
            logger.info("/groups/by_faculty.xml")

            res.type("application/xml")
            File("src/main/webapp/data/faculties.xml").readText()
        }

        get("/schedule/:group_id/:season") { req, res ->
            val groupId = req.params("group_id")
            val season = req.params("season")
            res.type("application/json")
            try {
                logger.info("/schedule/{}/{}", groupId, season)

                return@get getSchedule(groupId, season).json
            } catch (e: VyatsuScheduleException) {
                logger.error("/schedule/{}/{}: {}", groupId, season, e.message)

                res.status(422)
                return@get """{ "error": "${e.message}" }"""
            } catch (e: Exception) {
                logger.error("/schedule/{}/{}", groupId, season)
                logger.throwing(e)

                res.status(500)
                return@get """{ "error": "${e.message}" }"""
            }
        }
    }
}
