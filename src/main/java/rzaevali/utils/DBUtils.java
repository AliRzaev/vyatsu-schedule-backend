package rzaevali.utils;

import com.google.common.collect.ImmutableList;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import org.bson.Document;
import org.javatuples.Pair;
import rzaevali.exceptions.UnknownValueException;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static com.google.common.base.Preconditions.checkNotNull;

public class DBUtils {

    public static class DateRange implements Comparable<DateRange> {

        private String first;

        private String second;

        private LocalDate firstDate;

        DateRange(String first, String second) {
            this.first = first;
            this.second = second;
            this.firstDate = parseDate(first);
        }

        static List<String> toList(LocalDate first, LocalDate second) {
            String firstS = String.format(
                    "%02d%02d%04d",
                    first.getDayOfMonth(),
                    first.getMonthValue(),
                    first.getYear());
            String secondS = String.format(
                    "%02d%02d%04d",
                    second.getDayOfMonth(),
                    second.getMonthValue(),
                    second.getYear());

            return ImmutableList.of(firstS, secondS);
        }

        @Override
        public String toString() {
            return String.format("[%s, %s]", first, second);
        }

        @Override
        public int compareTo(DateRange o) {
            return this.firstDate.compareTo(o.firstDate);
        }
    }

    public static class ScheduleInfo {

        private List<List<List<String>>> weeks;

        private String groupId;

        private List<String> dateRange;

        private String season;

        public ScheduleInfo(List<List<List<String>>> weeks, String groupId, List<String> dateRange, String season) {
            checkNotNull(weeks);
            checkNotNull(groupId);
            checkNotNull(dateRange);
            checkNotNull(season);

            this.weeks = weeks;
            this.groupId = groupId;
            this.dateRange = dateRange;
            this.season = season;
        }

        public List<List<List<String>>> getWeeks() {
            return weeks;
        }

        public String getGroupId() {
            return groupId;
        }

        public List<String> getDateRange() {
            return dateRange;
        }

        public String getSeason() {
            return season;
        }
    }

    private static DBUtils instance = new DBUtils();

    private DBUtils() {
        dbUri = new MongoClientURI(System.getenv("MONGODB_URI"));
        dbClient = new MongoClient(dbUri);
    }

    public static DBUtils getInstance() {
        return instance;
    }

    private MongoClient dbClient;

    private MongoClientURI dbUri;

    private static final String GROUPS_LIST_URL =
            "https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html";

    /*
     * Document structure:
     * {
     *   groupId: "groupId",
     *   season: "season",
     *   range: ["first", "second"]
     * }
     * */
    private static final String DATE_RANGES_COLLECTION = "schedule_ranges";

    /*
     * Document structure:
     * {
     *   groupId: "groupId",
     *   group: "group_name", //deprecated
     *   season: "season",
     *   range: ["first", "second"],
     *   schedule: [
     *       [[], ... []], [[], ... []]
     *   ]
     * }
     * */
    private static final String SCHEDULE_COLLECTION = "schedules";

    /*
    * Document structure:
    * {
    *   groupId: "groupId",
    *   group: "group_name",
    *   faculty: "faculty_name"
    * }
    * */
    private static final String GROUPS_INFO_COLLECTION = "groups_info";

    public static final String SEASON_AUTUMN = "autumn";

    public static final String SEASON_SPRING = "spring";

    public String getGroupName(String groupId) throws UnknownValueException {
        checkNotNull(groupId, "groupId must not be null");

        MongoCollection<Document> collection =
                dbClient.getDatabase(dbUri.getDatabase()).getCollection(GROUPS_INFO_COLLECTION);

        BasicDBObject query = new BasicDBObject()
                .append("groupId", groupId);

        Document res = collection.find(query).first();
        if (res != null) {
            return res.getString("group");
        } else {
            throw new UnknownValueException(String.format("Unknown groupId: %s", groupId));
        }
    }

    List<String> getDateRange(String groupId, String season) throws UnknownValueException {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");
        checkSeason(season);

        MongoCollection<Document> collection =
                dbClient.getDatabase(dbUri.getDatabase()).getCollection(DATE_RANGES_COLLECTION);

        BasicDBObject query = new BasicDBObject()
                .append("groupId", groupId)
                .append("season", season);

        Document res = collection.find(query).first();
        if (res != null) {
            return (List<String>) res.get("range", List.class);
        } else {
            throw new UnknownValueException(String.format("Unknown groupId: %s", groupId));
        }
    }

    public void updateDateRanges(String season) throws UnknownValueException {
        checkNotNull(season, "season must not be null");
        checkSeason(season);

        try {
            MongoCollection<Document> collection =
                    dbClient.getDatabase(dbUri.getDatabase()).getCollection(DATE_RANGES_COLLECTION);

            getRangesFromSite(season).forEach((groupId, range) -> {
                BasicDBObject query = new BasicDBObject()
                        .append("groupId", groupId)
                        .append("season", season);

                List<String> listRange = DateRange.toList(range.getValue0(), range.getValue1());

                if (collection.find(query).first() != null) {
                    BasicDBObject value = new BasicDBObject()
                            .append("range", listRange);
                    BasicDBObject update = new BasicDBObject()
                            .append("$set", value);

                    collection.findOneAndUpdate(query, update);
                } else {
                    Document entry = new Document()
                            .append("groupId", groupId)
                            .append("season", season)
                            .append("range", listRange);
                    collection.insertOne(entry);
                }
            });
        } catch (UnirestException e) {
            e.printStackTrace();
        }
    }

    static String getSeasonKey(String season) throws UnknownValueException {
        checkNotNull(season, "season must not be null");
        checkSeason(season);

        return season.equals(SEASON_AUTUMN) ? "1" : "2";
    }

    public ScheduleInfo getCachedSchedule(String groupId, String season) throws UnknownValueException {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");
        checkSeason(season);

        MongoCollection<Document> collection =
                dbClient.getDatabase(dbUri.getDatabase()).getCollection(SCHEDULE_COLLECTION);

        BasicDBObject query = new BasicDBObject()
                .append("groupId", groupId)
                .append("season", season);

        Document res = collection.find(query).first();
        if (res != null) {
            List range = res.get("range", List.class);
            List weeks = res.get("schedule", List.class);

            return new ScheduleInfo(weeks, groupId, range, season);
        } else {
            return null;
        }
    }

    public void updateSchedule(ScheduleInfo scheduleInfo) throws UnknownValueException {
        checkNotNull(scheduleInfo, "schedule info must not be null");
        checkSeason(scheduleInfo.getSeason());

        MongoCollection<Document> collection =
                dbClient.getDatabase(dbUri.getDatabase()).getCollection(SCHEDULE_COLLECTION);

        BasicDBObject query = new BasicDBObject()
                .append("groupId", scheduleInfo.getGroupId())
                .append("season", scheduleInfo.getSeason());

        if (collection.find(query).first() != null) {
            BasicDBObject value = new BasicDBObject()
                    .append("range", scheduleInfo.getDateRange())
                    .append("schedule", scheduleInfo.getWeeks());
            BasicDBObject update = new BasicDBObject()
                    .append("$set", value);

            collection.findOneAndUpdate(query, update);
        } else {
            Document entry = new Document()
                    .append("groupId", scheduleInfo.getGroupId())
                    .append("season", scheduleInfo.getSeason())
                    .append("range", scheduleInfo.getDateRange())
                    .append("schedule", scheduleInfo.getWeeks());

            collection.insertOne(entry);
        }
    }

    private HashMap<String, Pair<LocalDate, LocalDate>> getRangesFromSite(String season) throws UnirestException, UnknownValueException {
        String seasonKey = getSeasonKey(season);
        String html = Unirest.get(GROUPS_LIST_URL).asString().getBody();
        Pattern pattern = Pattern.compile(String.format("/reports/schedule/Group/(\\d{4})_%s_(\\d{8})_(\\d{8})\\.pdf", seasonKey));
        Matcher matcher = pattern.matcher(html);

        HashMap<String, Pair<LocalDate, LocalDate>> dateRanges = new HashMap<>();
        while (matcher.find()) {
            String groupId = matcher.group(1);
            LocalDate first = parseDate(matcher.group(2));
            LocalDate second = parseDate(matcher.group(3));

            Pair<LocalDate, LocalDate> newRange = new Pair<>(first, second);
            Pair<LocalDate, LocalDate> oldRange = dateRanges.get(groupId);

            if (oldRange == null || oldRange.getValue0().compareTo(newRange.getValue0()) < 0) {
                dateRanges.put(groupId, newRange);
            }
        }

        return dateRanges;
    }

    private static String checkSeason(String season) throws UnknownValueException {
        if (!season.equals(SEASON_AUTUMN) && !season.equals(SEASON_SPRING)) {
            throw new UnknownValueException(String.format("Unknown season: %s", season));
        } else {
            return season;
        }
    }

    static LocalDate parseDate(String date) {
        int day = Integer.parseInt(date.substring(0, 2));
        int month = Integer.parseInt(date.substring(2, 4));
        int year = Integer.parseInt(date.substring(4));

        return LocalDate.of(year, month, day);
    }

}


