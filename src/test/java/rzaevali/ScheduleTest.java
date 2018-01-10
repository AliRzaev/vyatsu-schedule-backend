package rzaevali;

import com.google.common.collect.ImmutableList;
import org.junit.Test;
import rzaevali.exceptions.DocNotFoundException;
import rzaevali.exceptions.VyatsuScheduleException;
import rzaevali.utils.JsonUtils;
import rzaevali.utils.ScheduleUtils;

import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class ScheduleTest {

    @Test
    public void testParsing() throws IOException, VyatsuScheduleException {
        List<Integer> groupIds = ImmutableList.of(
                7795, 7794, 8891, 8969
        );

        String pathPattern = "src/test/resources/%s/%s_1_18122017_31122017.%s";

        for (Integer groupId : groupIds) {
            String pdfPath = String.format(pathPattern, "pdf", groupId, "pdf");
            String jsonPath = String.format(pathPattern, "json", groupId, "json");

            List data = ScheduleUtils.extractSchedule(Files.newInputStream(Paths.get(pdfPath)));
            List originalData = (List) JsonUtils.getDefaultJson()
                    .fromJson(new FileReader(jsonPath), Map.class).get("weeks");

            assertEquals(Integer.toString(groupId), originalData, data);
        }
    }

    @Test(expected = DocNotFoundException.class)
    public void testArgumentChecks() throws VyatsuScheduleException {
        ScheduleUtils.getSchedule("0000", "");
    }

    @Test
    public void testDateComparison() {
        List<String> firstDate = ImmutableList.of("11102017", "25102017");
        List<String> secondDate = ImmutableList.of("31102017", "13112017");

        assertTrue(ScheduleUtils.compareDates(firstDate, secondDate) < 1);
    }

}
