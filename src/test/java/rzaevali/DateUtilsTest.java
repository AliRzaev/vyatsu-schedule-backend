package rzaevali;

import com.google.common.collect.ImmutableList;
import org.junit.Test;
import rzaevali.utils.DateUtils;

import java.time.LocalDate;
import java.time.ZoneId;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class DateUtilsTest {

    @Test
    public void testDate() {
        for (int month = 1; month <= 7; ++month) {
            assertTrue(DateUtils.isSpring(LocalDate.of(2017, month, 1)));
        }

        for (int month = 8; month <= 12; ++month) {
            assertTrue(DateUtils.isAutumn(LocalDate.of(2017, month, 1)));
        }
    }

    @Test
    public void testDateComparison() {
        List<String> firstDate = ImmutableList.of("11102017", "25102017");
        List<String> secondDate = ImmutableList.of("31102017", "13112017");

        assertTrue(DateUtils.compareDates(firstDate, secondDate) < 1);
    }

    @Test
    public void testDateParsing() {
        LocalDate original = LocalDate.of(2018, 1, 2);
        LocalDate parsed = DateUtils.parseDate("02012018");

        assertEquals(original, parsed);
    }

}
