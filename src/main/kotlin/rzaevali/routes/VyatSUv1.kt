package rzaevali.routes

import org.apache.logging.log4j.LogManager
import org.litote.kmongo.json
import rzaevali.exceptions.VyatsuScheduleException
import rzaevali.utils.getSchedule
import spark.Spark.get
import spark.Spark.path

private val logger = LogManager.getLogger("vyatsu")

fun vyatsuRoutes() {
    path("/vyatsu") {
        get("/calls") { _, res ->
            logger.info("/calls")

            res.redirect("/static/v1/calls.json")
        }

        get("/groups.json") { _, res ->
            logger.info("/groups.json")

            res.redirect("/static/v1/groups.json")
        }

        get("/groups.xml") { _, res ->
            logger.info("/groups.xml")

            res.redirect("/static/v1/groups.xml")
        }

        get("/groups/by_faculty.json") { _, res ->
            logger.info("/groups/by_faculty.json")

            res.redirect("/static/v1/groups/by_faculty.json")
        }

        get("/groups/by_faculty.xml") { _, res ->
            logger.info("/groups/by_faculty.xml")

            res.redirect("/static/v1/groups/by_faculty.xml")
        }

        get("/schedule/:group_id/:season") { req, res ->
            val groupId = req.params("group_id")
            val season = req.params("season")

            LogsDao.insertOneLogRequest(groupId, season)

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
