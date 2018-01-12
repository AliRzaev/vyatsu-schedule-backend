package rzaevali;

import org.junit.Test;
import rzaevali.exceptions.UnknownValueException;
import rzaevali.utils.DBUtils;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

public class DBUtilsTest {

    private static final String INCORRECT_GROUP_ID = "null";

    private static final String INCORRECT_SEASON = "null";

    private static final String TEST_GROUP_ID = "0000";

    private static final String TEST_GROUP_NAME = "Test";

    @Test(expected = UnknownValueException.class)
    public void testArgumentChecks1() throws UnknownValueException {
        DBUtils.getInstance().getCachedSchedule(TEST_GROUP_ID, INCORRECT_SEASON);
    }

    @Test(expected = UnknownValueException.class)
    public void testArgumentChecks2() throws UnknownValueException {
        DBUtils.getInstance().updateDateRanges(INCORRECT_SEASON);
    }

    @Test
    public void testCachedSchedule() throws UnknownValueException {
        assertNull(DBUtils.getInstance().getCachedSchedule(INCORRECT_GROUP_ID, DBUtils.SEASON_AUTUMN));
        assertNull(DBUtils.getInstance().getCachedSchedule(INCORRECT_GROUP_ID, DBUtils.SEASON_SPRING));
    }

    @Test
    public void testExistentGroupId() throws UnknownValueException {
        String groupName = DBUtils.getInstance().getGroupName(TEST_GROUP_ID);
        assertEquals(groupName, TEST_GROUP_NAME);
    }

    @Test(expected = UnknownValueException.class)
    public void testNonExistentGroupId() throws UnknownValueException {
        DBUtils.getInstance().getGroupName(INCORRECT_GROUP_ID);
    }

}
