@file:JvmName("Main")

package rzaevali.heroku

import rzaevali.routes.vyatsuRoutes
import rzaevali.routes.vyatsuV2Routes
import spark.Spark.*

fun main(args: Array<String>) {
    val defaultPort = "8080"
    val portVar = System.getenv("PORT") ?: ""
    val port = if (portVar.isEmpty()) {
        defaultPort
    } else {
        portVar
    }

    port(port.toInt())

    staticFiles.location("/public")
    staticFiles.header("Access-Control-Allow-Origin", "*")
    staticFiles.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")

    after("/*") { _, res ->
        res.header("Access-Control-Allow-Origin", "*")
        res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
    }
    vyatsuRoutes()
    vyatsuV2Routes()
}
