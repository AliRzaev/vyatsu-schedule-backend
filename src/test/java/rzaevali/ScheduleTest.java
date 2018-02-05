package rzaevali;

import com.google.common.collect.ImmutableList;
import org.junit.Test;
import rzaevali.exceptions.UnknownValueException;
import rzaevali.exceptions.VyatsuScheduleException;
import rzaevali.utils.JsonUtils;
import rzaevali.utils.PdfUtils;
import rzaevali.utils.ScheduleUtilsKt;

import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.assertEquals;

public class ScheduleTest {

    private static final String INCORRECT_SEASON = "null";

    private static final String TEST_GROUP_ID = "0000";

    @Test
    public void testParsing() throws IOException, VyatsuScheduleException {
        List<Integer> groupIds = ImmutableList.of(
                7795, 7794, 8891, 8969
        );

        String pathPattern = "src/test/resources/%s/%s_1_18122017_31122017.%s";

        for (Integer groupId : groupIds) {
            String pdfPath = String.format(pathPattern, "pdf", groupId, "pdf");
            String jsonPath = String.format(pathPattern, "json", groupId, "json");

            List data = PdfUtils.INSTANCE.extractSchedule(Files.newInputStream(Paths.get(pdfPath)));
            List originalData = (List) JsonUtils.getDefaultJson()
                    .fromJson(new FileReader(jsonPath), Map.class).get("weeks");

            assertEquals(Integer.toString(groupId), originalData, data);
        }
    }

    @Test(expected = UnknownValueException.class)
    public void testArgumentChecks() throws VyatsuScheduleException {
        ScheduleUtilsKt.getSchedule(TEST_GROUP_ID, INCORRECT_SEASON);
    }

}
