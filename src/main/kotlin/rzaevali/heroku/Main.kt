@file:JvmName("Main")

package rzaevali.heroku

import rzaevali.routes.VyatSUv1
import rzaevali.routes.VyatSUv2

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
    VyatSUv1.setRoutes()
    VyatSUv2.setRoutes()
}
