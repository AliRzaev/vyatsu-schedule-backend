package rzaevali.dao

import com.mongodb.BasicDBObject
import org.litote.kmongo.MongoOperator.set
import org.litote.kmongo.findOne
import org.litote.kmongo.getCollection
import rzaevali.utils.NestedList
import rzaevali.utils.getDatabase

data class ScheduleInfo(
        val groupId: String,
        val season: String,
        val range: List<String>,
        val schedule: NestedList)

object ScheduleInfoDao {

    private const val SCHEDULE_COLLECTION = "schedules"

    private const val GROUP_ID_FIELD = "groupId"

    private const val SEASON_FIELD = "season"

    private const val RANGE_FIELD = "range"

    private const val SCHEDULE_FIELD = "schedule"

    fun findByGroupIdAndSeason(groupId: String, season: String): ScheduleInfo? {
        val collection = getDatabase()
                .getCollection<ScheduleInfo>(SCHEDULE_COLLECTION)

        val query = BasicDBObject()
        query[GROUP_ID_FIELD] = groupId
        query[SEASON_FIELD] = season

        return collection.findOne(query)
    }

    fun insertOneOrUpdate(groupId: String, season: String, range: List<String>, schedule: NestedList) {
        val collection = getDatabase()
                .getCollection<ScheduleInfo>(SCHEDULE_COLLECTION)

        val query = BasicDBObject()
        query[GROUP_ID_FIELD] = groupId
        query[SEASON_FIELD] = season

        if (collection.findOne(query) != null) {
            val update = BasicDBObject()
            update["$set"] = BasicDBObject()
                    .append(RANGE_FIELD, range)
                    .append(SCHEDULE_FIELD, schedule)

            collection.findOneAndUpdate(query, update)
        } else {
            collection.insertOne(
                    ScheduleInfo(groupId, season, range, schedule)
            )
        }
    }

}