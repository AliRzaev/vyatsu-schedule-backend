package rzaevali.utils;

import com.google.common.collect.ImmutableList;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

import java.time.LocalDate;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.javatuples.Pair;
import rzaevali.exceptions.DocNotFoundException;
import rzaevali.utils.ScheduleUtils.Schedule;

import static com.google.common.base.Preconditions.checkArgument;
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

        public List<String> toList() {
            return ImmutableList.of(first, second);
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

        String getFirst() {
            return first;
        }

        String getSecond() {
            return second;
        }

        @Override
        public int compareTo(DateRange o) {
            return this.firstDate.compareTo(o.firstDate);
        }
    }

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
    *   group: "group_name",
    *   season: "season",
    *   range: ["first", "second"],
    *   schedule: [
    *       [[], ... []], [[], ... []]
    *   ]
    * }
    * */
    private static final String SCHEDULE_COLLECTION = "schedules";

    public static final String SEASON_AUTUMN = "autumn";

    public static final String SEASON_SPRING = "spring";

    static List<String> getDateRange(String groupId, String season) throws DocNotFoundException {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");
        checkArgument(
                season.equals(SEASON_SPRING) ||
                        season.equals(SEASON_AUTUMN)
        );

        MongoClientURI uri = new MongoClientURI(System.getenv("MONGODB_URI"));

        try (MongoClient client = new MongoClient(uri)) {
            MongoDatabase db = client.getDatabase(uri.getDatabase());
            MongoCollection<Document> collection = db.getCollection(DATE_RANGES_COLLECTION);

            BasicDBObject query = new BasicDBObject();
            query.put("groupId", groupId);
            query.put("season", season);

            Document res = collection.find(query).first();
            if (res != null) {
                return (List<String>) res.get("range");
            } else {
                throw new DocNotFoundException(String.format("Unknown parameter groupId: %s", groupId));
            }
        }
    }

    public static void updateDateRanges(String season) throws DocNotFoundException {
        checkNotNull(season);

        if (!season.equals(SEASON_AUTUMN) && !season.equals(SEASON_SPRING)) {
            throw new DocNotFoundException("Unknown parameter season");
        }

        MongoClientURI uri = new MongoClientURI(System.getenv("MONGODB_URI"));

        try (MongoClient client = new MongoClient(uri)) {
            MongoDatabase db = client.getDatabase(uri.getDatabase());
            MongoCollection<Document> collection = db.getCollection(DATE_RANGES_COLLECTION);

            getRangesFromSite(season).forEach((groupId, range) -> {
                BasicDBObject query = new BasicDBObject();
                query.put("groupId", groupId);
                query.put("season", season);

                List<String> listRange = DateRange.toList(range.getValue0(), range.getValue1());

                if (collection.find(query).first() != null) {
                    BasicDBObject update = new BasicDBObject();
                    BasicDBObject value = new BasicDBObject();
                    value.put("range", listRange);
                    update.put("$set", value);
                    collection.findOneAndUpdate(query, update);
                } else {
                    Document entry = new Document();
                    entry.put("groupId", groupId);
                    entry.put("season", season);
                    entry.put("range", listRange);
                    collection.insertOne(entry);
                }
            });

        } catch (UnirestException e) {
            e.printStackTrace();
        }
    }

    static String getSeasonKey(String season) {
        checkNotNull(season, "season must not be null");
        checkArgument(
                season.equals(SEASON_SPRING) ||
                        season.equals(SEASON_AUTUMN)
        );

        return season.equals(SEASON_AUTUMN) ? "1" : "2";
    }

    public static Schedule getCachedSchedule(String groupId, String season) throws DocNotFoundException {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");

        if (!season.equals(SEASON_AUTUMN) && !season.equals(SEASON_SPRING)) {
            throw new DocNotFoundException("Unknown parameter season");
        }

        MongoClientURI uri = new MongoClientURI(System.getenv("MONGODB_URI"));

        try (MongoClient client = new MongoClient(uri)) {
            MongoDatabase db = client.getDatabase(uri.getDatabase());
            MongoCollection<Document> collection = db.getCollection(SCHEDULE_COLLECTION);

            BasicDBObject query = new BasicDBObject();
            query.put("groupId", groupId);
            query.put("season", season);

            Document res = collection.find(query).first();
            if (res != null) {
                List range =  res.get("range", List.class);
                List weeks = res.get("schedule", List.class);
                String group = res.getString("group");

                return new Schedule(weeks, group, range);
            } else {
                return null;
            }
        } catch (Exception ignore) {
            return null;
        }
    }

    public static void updateSchedule(String groupId, String season, Schedule schedule) throws DocNotFoundException {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");
        checkNotNull(schedule, "schedule must not be null");

        if (!season.equals(SEASON_AUTUMN) && !season.equals(SEASON_SPRING)) {
            throw new DocNotFoundException("Unknown parameter season");
        }

        MongoClientURI uri = new MongoClientURI(System.getenv("MONGODB_URI"));

        try (MongoClient client = new MongoClient(uri)) {
            MongoDatabase db = client.getDatabase(uri.getDatabase());
            MongoCollection<Document> collection = db.getCollection(SCHEDULE_COLLECTION);

            BasicDBObject query = new BasicDBObject();
            query.put("groupId", groupId);
            query.put("season", season);

            BasicDBObject update = new BasicDBObject();
            BasicDBObject value = new BasicDBObject();

            value.put("range", schedule.getDateRange());
            value.put("schedule", schedule.getWeeks());

            update.put("$set", value);

            if (collection.find(query).first() != null) {
                collection.findOneAndUpdate(query, update);
            } else {
                Document entry = new Document();
                entry.put("groupId", groupId);
                entry.put("group", schedule.getGroup());
                entry.put("season", season);
                entry.put("range", schedule.getDateRange());
                entry.put("schedule", schedule.getWeeks());
                collection.insertOne(entry);
            }
        } catch (Exception ignore) {
        }
    }

    private static HashMap<String, Pair<LocalDate, LocalDate>> getRangesFromSite(String season) throws UnirestException {
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

    static LocalDate parseDate(String date) {
        int day = Integer.parseInt(date.substring(0, 2));
        int month = Integer.parseInt(date.substring(2, 4));
        int year = Integer.parseInt(date.substring(4));

        return LocalDate.of(year, month, day);
    }

}


