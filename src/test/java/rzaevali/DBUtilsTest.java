package rzaevali;

import org.junit.Test;
import rzaevali.exceptions.DocNotFoundException;
import rzaevali.utils.DBUtils;

import static org.junit.Assert.assertNull;

public class DBUtilsTest {

    @Test(expected = DocNotFoundException.class)
    public void testArgumentChecks1() throws DocNotFoundException {
        DBUtils.getCachedSchedule("0000", "");
    }

    @Test(expected = DocNotFoundException.class)
    public void testArgumentChecks2() throws DocNotFoundException {
        DBUtils.updateDateRanges("");
    }

    @Test
    public void testCachedSchedule() throws DocNotFoundException {
        assertNull(DBUtils.getCachedSchedule("", DBUtils.SEASON_AUTUMN));
        assertNull(DBUtils.getCachedSchedule("", DBUtils.SEASON_SPRING));
    }

}
