package rzaevali.dao

import com.mongodb.BasicDBObject
import org.litote.kmongo.MongoOperator.set
import org.litote.kmongo.findOne
import org.litote.kmongo.getCollection
import rzaevali.exceptions.UnknownValueException
import rzaevali.utils.getDatabase

data class GroupInfo(val groupId: String, val group: String, val faculty: String)

object GroupsInfoDao {

    private const val GROUPS_INFO_COLLECTION = "groups_info"

    private const val GROUP_ID_FIELD = "groupId"

    @Throws(UnknownValueException::class)
    fun findByGroupId(groupId: String): GroupInfo {
        val collection = getDatabase().getCollection<GroupInfo>(GROUPS_INFO_COLLECTION)

        val query = BasicDBObject()
        query[GROUP_ID_FIELD] = groupId

        val res = collection.findOne(query)
        if (res != null) {
            return res
        } else {
            throw UnknownValueException("Unknown groupId: $groupId")
        }
    }

    fun insertOneOrUpdate(groupId: String, group: String, faculty: String) {
        val collection = getDatabase().getCollection<GroupInfo>(GROUPS_INFO_COLLECTION)

        val query = BasicDBObject()
        query[GROUP_ID_FIELD] = groupId

        val item = GroupInfo(groupId, group, faculty)

        if (collection.findOne(query) != null) {
            val update = BasicDBObject()
            update["$set"] = item
            collection.findOneAndUpdate(query, update)
        } else {
            collection.insertOne(item)
        }
    }

}