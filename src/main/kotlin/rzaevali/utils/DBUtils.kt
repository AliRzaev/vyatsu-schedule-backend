package rzaevali.utils

import com.mongodb.MongoClientURI
import com.mongodb.client.MongoDatabase
import org.litote.kmongo.KMongo

private val dbUri = MongoClientURI(System.getenv("MONGODB_URI"))

private val dbClient = KMongo.createClient(dbUri)

private val database = dbClient.getDatabase(dbUri.database)

fun getDatabase(): MongoDatabase = database
