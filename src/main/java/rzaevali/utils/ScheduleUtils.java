package rzaevali.utils;

import org.apache.pdfbox.pdmodel.PDDocument;
import rzaevali.exceptions.DocNotFoundException;
import rzaevali.utils.DBUtils.*;
import technology.tabula.*;
import technology.tabula.extractors.ExtractionAlgorithm;
import technology.tabula.extractors.SpreadsheetExtractionAlgorithm;

import java.io.IOException;
import java.net.URL;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import static com.google.common.base.Preconditions.checkNotNull;
import static rzaevali.utils.DBUtils.*;

public class ScheduleUtils {

    private static final String BASE_URL = "https://www.vyatsu.ru/reports/schedule/Group/%s_%s_%s_%s.pdf";

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
    }

    public static String getSchedule(String groupId, String season) throws IOException,
                                                                             DocNotFoundException {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");

        if (!season.equals(SEASON_AUTUMN) && !season.equals(SEASON_SPRING)) {
            throw new DocNotFoundException("Invalid param season");
        }

        Schedule cachedSchedule = ScheduleCache.getInstance().getSchedule(groupId, season);

        DateRange range = DBUtils.getDateRange(groupId, season);

        if (cachedSchedule == null) {
            Schedule schedule = getScheduleFromSite(groupId, season, range);
            ScheduleCache.getInstance().updateSchedule(groupId, season, schedule);

            return dumpSchedule(schedule);
        } else {
            LocalDate date = parseDate(range.getFirst());
            LocalDate cachedDate = parseDate(cachedSchedule.getDateRange().get(0));

            if (date.compareTo(cachedDate) > 0) {
                Schedule schedule = getScheduleFromSite(groupId, season, range);
                ScheduleCache.getInstance().updateSchedule(groupId, season, schedule);

                return dumpSchedule(schedule);
            } else {
                return dumpSchedule(cachedSchedule);
            }
        }
    }

    private static String dumpSchedule(Schedule schedule) {
        if (System.getenv("DEBUG") != null) {
            return JsonUtils.PRETTY_JSON.toJson(schedule);
        } else {
            return JsonUtils.STANDARD_JSON.toJson(schedule);
        }
    }

    private static Schedule getScheduleFromSite(String groupId, String season, DateRange range) throws IOException {
        URL url = new URL(String.format(BASE_URL, groupId, getSeasonKey(season), range.getFirst(), range.getSecond()));
        List<String> rows = parsePDFFile(url);
        List<List<String>> days = new ArrayList<>();
        for (int i = 0; i < 14; ++i) {
            days.add(new ArrayList<>());
        }

        for (int i = 2; i < rows.size(); i += 7) {
            List<String> day = days.get((i - 2) / 7);
            for (int j = i; j < i + 7; ++j) {
                day.add(rows.get(j));
            }
        }

        String group = rows.get(1).split(" ")[2];
        List<List<List<String>>> weeks = new ArrayList<>();
        weeks.add(days.subList(0, 6));
        weeks.add(days.subList(7, 13));

        return new Schedule(weeks, group, range.toList());
    }

    private static List<String> parsePDFFile(URL url) throws IOException {
        try (PDDocument pdfDocument = PDDocument.load(url.openStream())) {
            PageIterator pageIterator = new ObjectExtractor(pdfDocument).extract();
            ExtractionAlgorithm algorithm = new SpreadsheetExtractionAlgorithm();
            List<Table> tables = new ArrayList<>();

            while (pageIterator.hasNext()) {
                Page page = pageIterator.next();
                tables.addAll(algorithm.extract(page));
            }

            return tables.stream()
                    .flatMap(table -> table.getRows().stream())
                    .map(row -> row.stream()
                            .map(RectangularTextContainer::getText)
                            .filter(text -> !text.equals(""))
                            .collect(Collectors.joining(" ")))
                    .map(text -> text.replaceFirst("\\d{2}:\\d{2}-\\d{2}:\\d{2}\\s*", ""))
                    .collect(Collectors.toList());
        }
    }

}
