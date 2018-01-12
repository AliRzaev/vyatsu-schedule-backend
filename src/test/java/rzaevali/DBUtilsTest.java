package rzaevali;

import org.junit.Test;
import rzaevali.exceptions.UnknownValueException;
import rzaevali.utils.DBUtils;

import static org.junit.Assert.assertNull;

public class DBUtilsTest {

    @Test(expected = UnknownValueException.class)
    public void testArgumentChecks1() throws UnknownValueException {
        DBUtils.getInstance().getCachedSchedule("0000", "");
    }

    @Test(expected = UnknownValueException.class)
    public void testArgumentChecks2() throws UnknownValueException {
        DBUtils.getInstance().updateDateRanges("");
    }

    @Test
    public void testCachedSchedule() throws UnknownValueException {
        assertNull(DBUtils.getInstance().getCachedSchedule("", DBUtils.SEASON_AUTUMN));
        assertNull(DBUtils.getInstance().getCachedSchedule("", DBUtils.SEASON_SPRING));
    }

}
