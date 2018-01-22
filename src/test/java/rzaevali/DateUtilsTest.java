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
        LocalDate date = LocalDate.now(ZoneId.of("Europe/Moscow"));

        boolean isAutumn = DateUtils.isAutumn(date);
        boolean isSpring = DateUtils.isSpring(date);

        assertTrue(isAutumn != isSpring);
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
