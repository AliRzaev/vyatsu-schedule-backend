package rzaevali.utils;

import com.google.common.io.CharStreams;
import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.time.LocalDate;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import rzaevali.exceptions.DocNotFoundException;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public class DBUtils {

    public static class DateRange {

        private String first;

        private String second;

        DateRange(String first, String second) {
            this.first = first;
            this.second = second;
        }

        public List<String> toList() {
            List<String> list = new ArrayList<>();
            list.add(first);
            list.add(second);
            return list;
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

            List<String> list = new ArrayList<>();
            list.add(firstS);
            list.add(secondS);

            return list;
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

    }

    private static final String GROUPS_LIST_URL =
            "https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html";

    private static final String DATE_RANGES_COLLECTION = "schedule_ranges";

    private static final String SEASON_AUTUMN = "autumn";

    private static final String SEASON_SPRING = "spring";

    static DateRange getDateRange(String groupId, String season) throws DocNotFoundException {
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
                List<String> range = (List<String>) res.get("range");
                return new DateRange(range.get(0), range.get(1));
            } else {
                throw new DocNotFoundException(String.format("No doc with such groupId: %s", groupId));
            }
        }
    }

    public static void updateDateRanges(String season) {
        checkArgument(season.equals(SEASON_SPRING) || season.equals(SEASON_AUTUMN));

        MongoClientURI uri = new MongoClientURI(System.getenv("MONGODB_URI"));

        try (MongoClient client = new MongoClient(uri)) {
            MongoDatabase db = client.getDatabase(uri.getDatabase());
            MongoCollection<Document> collection = db.getCollection(DATE_RANGES_COLLECTION);

            HashMap<String, Map.Entry<LocalDate, LocalDate>> dateRanges = getRangesFromSite(season);

            for (String groupId : dateRanges.keySet()) {

                BasicDBObject query = new BasicDBObject();
                query.put("groupId", groupId);
                query.put("season", season);

                BasicDBObject update = new BasicDBObject();
                BasicDBObject value = new BasicDBObject();
                value.put("range", getMaxRange(dateRanges, groupId));
                update.put("$set", value);

                if (collection.find(query).first() != null) {
                    collection.findOneAndUpdate(query, update);
                } else {
                    Document entry = new Document();
                    entry.put("groupId", groupId);
                    entry.put("season", season);
                    entry.put("range", getMaxRange(dateRanges, groupId));
                    collection.insertOne(entry);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static List<String> getMaxRange(HashMap<String, Map.Entry<LocalDate, LocalDate>> map, String groupId) {
        Map.Entry<LocalDate, LocalDate> e = map.get(groupId);

        return DateRange.toList(e.getKey(), e.getValue());
    }

    private static HashMap<String, Map.Entry<LocalDate, LocalDate>> getRangesFromSite(String season) throws IOException {
        String seasonKey = season.equals(SEASON_AUTUMN) ? "1" : "2";
        URL url = new URL(GROUPS_LIST_URL);
        String html = CharStreams.toString(new InputStreamReader(url.openStream()));
        Pattern pattern = Pattern.compile(String.format("/reports/schedule/Group/(\\d{4})_%s_(\\d{8})_(\\d{8})\\.pdf", seasonKey));
        Matcher matcher = pattern.matcher(html);

        HashMap<String, Map.Entry<LocalDate, LocalDate>> dateRanges = new HashMap<>();
        while (matcher.find()) {
            String groupId = matcher.group(1);
            LocalDate first = parseDate(matcher.group(2));
            LocalDate second = parseDate(matcher.group(3));

            Map.Entry<LocalDate, LocalDate> newRange = new AbstractMap.SimpleEntry<>(first, second);
            Map.Entry<LocalDate, LocalDate> oldRange = dateRanges.get(groupId);

            if (oldRange == null || oldRange.getKey().compareTo(newRange.getKey()) < 0) {
                dateRanges.put(groupId, newRange);
            }
        }

        return dateRanges;
    }

    private static LocalDate parseDate(String date) {
        int day = Integer.parseInt(date.substring(0, 2));
        int month = Integer.parseInt(date.substring(2, 4));
        int year = Integer.parseInt(date.substring(4));

        return LocalDate.of(year, month, day);
    }

}


