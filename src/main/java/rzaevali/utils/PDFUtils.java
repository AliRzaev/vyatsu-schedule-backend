package rzaevali.utils;

import com.google.gson.GsonBuilder;
import org.apache.pdfbox.pdmodel.PDDocument;
import technology.tabula.*;
import technology.tabula.extractors.ExtractionAlgorithm;
import technology.tabula.extractors.SpreadsheetExtractionAlgorithm;

import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import rzaevali.exceptions.DocNotFoundException;

import static com.google.common.base.Preconditions.checkNotNull;
import static com.google.common.base.Preconditions.checkArgument;

public class PDFUtils {
    private static final String BASE_URL = "https://www.vyatsu.ru/reports/schedule/Group/%s_1_%s_%s.pdf";

    private static class Schedule {
        private List<List<List<String>>> weeks;
        private String group;

        Schedule(List<List<List<String>>> weeks, String group) {
            this.weeks = weeks;
            this.group = group;
        }
    }

    public static String parseSchedule(String groupId, String season) throws IOException,
                                                                             DocNotFoundException {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");

        DBUtils.DateRange range = DBUtils.getDateRange(groupId, season);

        URL url = new URL(String.format(BASE_URL, groupId, range.getFirst(), range.getSecond()));
        List<String> rows = parsePDFFile(url);
        List<List<String>> days = new ArrayList<>();
        for (int i = 0; i < 14; ++i) {
            days.add(new ArrayList<String>());
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

        return new GsonBuilder().
                setPrettyPrinting().
                create().
                toJson(new Schedule(weeks, group));
    }

    private static List<String> parsePDFFile(URL url) throws IOException {
        PDDocument pdfDocument = PDDocument.load(url.openStream());
        PageIterator pageIterator = new ObjectExtractor(pdfDocument).extract();
        ExtractionAlgorithm algorithm = new SpreadsheetExtractionAlgorithm();
        List<Table> tables = new ArrayList<>();
        List<String> rows = new ArrayList<>();

        while (pageIterator.hasNext()) {
            Page page = pageIterator.next();
            tables.addAll(algorithm.extract(page));
        }


        for (Table table : tables) {
            List<List<RectangularTextContainer>> currentRows = table.getRows();
            for (List<RectangularTextContainer> row : currentRows) {
                StringBuilder stringBuilder = new StringBuilder("");
                for (RectangularTextContainer column : row) {
                    String text = column.getText();
                    if (text.equals("")) {
                        continue;
                    }
                    stringBuilder.append(text);
                    stringBuilder.append(' ');
                }

                rows.add(stringBuilder.toString().replaceFirst("\\d{2}:\\d{2}-\\d{2}:\\d{2}\\s*", ""));
            }
        }

        return rows;
    }

}
