package rzaevali.utils;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.Streams;
import org.apache.pdfbox.pdmodel.PDDocument;
import rzaevali.exceptions.PdfFileFormatException;
import rzaevali.exceptions.PdfFileProcessingException;
import rzaevali.exceptions.VyatsuScheduleException;
import rzaevali.exceptions.VyatsuServerException;
import technology.tabula.ObjectExtractor;
import technology.tabula.PageIterator;
import technology.tabula.RectangularTextContainer;
import technology.tabula.extractors.ExtractionAlgorithm;
import technology.tabula.extractors.SpreadsheetExtractionAlgorithm;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static com.google.common.base.Preconditions.checkNotNull;

public class PdfUtils {

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

    public static List<List<List<String>>> extractSchedule(String url) throws VyatsuScheduleException {
        checkNotNull(url);

        try {
            return extractSchedule(new URL(url).openStream());
        } catch (IOException ignore) {
            throw new VyatsuServerException("vyatsu.ru server error");
        }
    }

}
