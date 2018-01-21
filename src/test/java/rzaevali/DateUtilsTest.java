package rzaevali;

import org.junit.Test;
import static org.junit.Assert.*;
import rzaevali.utils.DateUtils;

import java.time.LocalDate;
import java.time.ZoneId;

public class DateUtilsTest {

    @Test
    public void testDate() {
        LocalDate date = LocalDate.now(ZoneId.of("Europe/Moscow"));

        boolean isAutumn = DateUtils.isAutumn(date);
        boolean isSpring = DateUtils.isSpring(date);

        assertTrue(isAutumn != isSpring);
    }

}
