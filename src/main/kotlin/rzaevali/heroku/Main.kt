@file:JvmName("Main")

package rzaevali.heroku

import rzaevali.routes.vyatsuRoutes
import rzaevali.routes.vyatsuV2Routes

import spark.Spark.port

fun main(args: Array<String>) {
    val defaultPort = "8080"
    val portVar = System.getenv("PORT") ?: ""
    val port = if (portVar.isEmpty()) {
        defaultPort
    } else {
        portVar
    }

    port(port.toInt())
    vyatsuRoutes()
    vyatsuV2Routes()
}
