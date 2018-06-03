package rzaevali.dao

import com.mongodb.BasicDBObject
import org.litote.kmongo.*
import org.litote.kmongo.MongoOperator.*
import rzaevali.exceptions.UnknownValueException
import rzaevali.utils.getDatabase

data class DateRange(val groupId: String, val season: String, val range: List<String>)

object DateRangesDao {

    private const val DATE_RANGES_COLLECTION = "schedule_ranges"

    private const val GROUP_ID_FIELD = "groupId"

    private const val SEASON_FIELD = "season"

    private const val RANGE_FIELD = "range"

    @Throws(UnknownValueException::class)
    fun findByGroupIdAndSeason(groupId: String, season: String): DateRange {
        val collection = getDatabase()
                .getCollection<DateRange>(DATE_RANGES_COLLECTION)

        val query = BasicDBObject()
        query[GROUP_ID_FIELD] = groupId
        query[SEASON_FIELD] = season

        val res = collection.findOne(query)
        if (res != null) {
            return res
        } else {
            throw UnknownValueException("Unknown groupId: $groupId")
        }
    }

    fun insertOneOrUpdate(groupId: String, season: String, range: Pair<String, String>) {
        val collection = getDatabase()
                .getCollection<DateRange>(DATE_RANGES_COLLECTION)

        val query = BasicDBObject()
        query[GROUP_ID_FIELD] = groupId
        query[SEASON_FIELD] = season

        if (collection.findOne(query) != null) {
            val update = BasicDBObject()
            update["$set"] = BasicDBObject()
                    .append(RANGE_FIELD, range.toList())

            collection.findOneAndUpdate(query, update)
        } else {
            val entry = DateRange(groupId, season, range.toList())
            collection.insertOne(entry)
        }
    }

}