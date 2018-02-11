@file:JvmName("GroupsInfoUpdater")

package rzaevali.updater

import com.mashape.unirest.http.Unirest
import org.jsoup.Jsoup
import rzaevali.dao.GroupsInfoDao

private const val URL = "https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html"

fun main(args: Array<String>) {
    val groups = getGroupsFromSite(URL)

    groups.forEach { groupInfo ->
        GroupsInfoDao.insertOneOrUpdate(groupInfo.first, groupInfo.second, groupInfo.third)
    }
}


private fun getGroupsFromSite(url: String): Set<Triple<String, String, String>> {
    val document = Jsoup.parse(Unirest.get(url).asString().body)
    val tables = document
            .selectFirst("div.column-center_rasp")
            .children()
            .select("""table[style="border: none !important;"]""")

    return tables
            .asSequence()
            .flatMap { tableTag ->
                tableTag.selectFirst("tbody")
                        .children()
                        .asSequence()
                        .flatMap { facultyTag ->
                            val facultyName = facultyTag.selectFirst("div.fak_name").text()
                            facultyTag.select("div.grpPeriod")
                                    .asSequence()
                                    .map { groupTag ->
                                        val groupName = groupTag.text().substringBefore('(')
                                        val groupPeriodId = groupTag.attr("data-grp_period_id")
                                        val groupId = groupPeriodId.slice(0 until groupPeriodId.lastIndex)
                                        Triple(groupId, groupName, facultyName)
                                    }
                        }
            }
            .toSet()
}