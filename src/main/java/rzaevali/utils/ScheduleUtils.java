package rzaevali.utils;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.Streams;
import org.apache.pdfbox.pdmodel.PDDocument;
import rzaevali.exceptions.*;
import rzaevali.utils.DBUtils.*;
import technology.tabula.*;
import technology.tabula.extractors.ExtractionAlgorithm;
import technology.tabula.extractors.SpreadsheetExtractionAlgorithm;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.time.LocalDate;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;
import static rzaevali.utils.DBUtils.*;

public class ScheduleUtils {

    private static final String BASE_URL = "https://www.vyatsu.ru/reports/schedule/Group/%s_%s_%s_%s.pdf";

    private static final boolean SCHEDULE_CACHE_ENABLED = Objects.equals(System.getenv("SCHEDULE_CACHE"), "enabled");

    static class Schedule {

        private List<List<List<String>>> weeks;

        private String group;

        private List<String> date_range;

        Schedule(List<List<List<String>>> weeks, String group, List<String> date_range) {
            this.weeks = weeks;
            this.group = group;
            this.date_range = date_range;
        }

        List<String> getDateRange() {
            return date_range;
        }

        public List<List<List<String>>> getWeeks() {
            return weeks;
        }

        public String getGroup() {
            return group;
        }

    }

    public static int compareDates(List<String> first, List<String> second) {
        checkArgument(first.size() == 2);
        checkArgument(second.size() == 2);

        LocalDate firstDate = parseDate(first.get(0));
        LocalDate secondDate = parseDate(second.get(0));

        return firstDate.compareTo(secondDate);
    }

    public static String getSchedule(String groupId, String season) throws VyatsuScheduleException {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");

        if (!season.equals(SEASON_AUTUMN) && !season.equals(SEASON_SPRING)) {
            throw new DocNotFoundException("Unknown parameter season");
        }

        List<String> range = DBUtils.getDateRange(groupId, season);
        String group = getGroupName(groupId);
        String url = buildUrl(groupId, season, range);

        if (!SCHEDULE_CACHE_ENABLED) {
            return JsonUtils.schedule(
                    extractSchedule(url),
                    group,
                    range
            );
        }

        Schedule cachedSchedule = DBUtils.getCachedSchedule(groupId, season);

        if (cachedSchedule == null || compareDates(range, cachedSchedule.getDateRange()) > 0) {
            Schedule schedule = new Schedule(
                    extractSchedule(url),
                    group,
                    range
            );
            DBUtils.updateSchedule(groupId, season, schedule);

            return JsonUtils.schedule(schedule);
        } else {
            return JsonUtils.schedule(cachedSchedule);
        }
    }

    private static String buildUrl(String groupId, String season, List<String> range) {
        return String.format(
                BASE_URL,
                groupId,
                getSeasonKey(season),
                range.get(0),
                range.get(1)
        );
    }

    public static String getGroupName(String groupId) {
        checkNotNull(groupId, "groupId must not be null");

        return "";
    }

    public static List<List<List<String>>> extractSchedule(String url) throws VyatsuScheduleException {
        checkNotNull(url);

        try {
            return extractSchedule(new URL(url).openStream());
        } catch (IOException ignore) {
            throw new VyatsuServerException("vyatsu.ru server error");
        }
    }

    public static List<List<List<String>>> extractSchedule(InputStream stream) throws VyatsuScheduleException {
        checkNotNull(stream);

        final int DAYS_COUNT = 14;
        final int LESSONS_PER_DAY = 7;

        List<String> rows = extractRows(stream);
        if (rows.size() != DAYS_COUNT * LESSONS_PER_DAY) {
            throw new PdfFileFormatException("Invalid pdf file");
        }

        List<List<String>> days = IntStream.range(0, 14)
                .mapToObj(day -> {
                    int fromIndex = day * 7;
                    int toIndex = fromIndex + 7;
                    return rows.subList(fromIndex, toIndex);
                })
                .collect(Collectors.toList());

        return ImmutableList.of(
                days.subList(0, 6),
                days.subList(7, 13)
        );
    }

    private static List<String> extractRows(InputStream stream) throws PdfFileProcessingException {
        try (PDDocument pdfDocument = PDDocument.load(stream)) {
            PageIterator pageIterator = new ObjectExtractor(pdfDocument).extract();
            ExtractionAlgorithm algorithm = new SpreadsheetExtractionAlgorithm();

            return Streams.stream(pageIterator)
                    .flatMap(page -> algorithm.extract(page).stream())
                    .flatMap(table -> table.getRows().stream())
                    .map(row -> row.stream()
                            .map(RectangularTextContainer::getText)
                            .filter(text -> !text.equals(""))
                            .collect(Collectors.joining(" ")))
                    .map(text -> text.replaceFirst("\\d{2}:\\d{2}-\\d{2}:\\d{2}\\s*", ""))
                    .skip(2)
                    .collect(Collectors.toList());
        } catch (Exception ignore) {
            throw new PdfFileProcessingException("Error while processing pdf file");
        }
    }

}
