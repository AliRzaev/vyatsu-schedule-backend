package rzaevali;

import org.junit.Test;
import rzaevali.exceptions.UnknownValueException;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static rzaevali.utils.DBUtilsKt.*;

public class DBUtilsTest {

    private static final String INCORRECT_GROUP_ID = "null";

    private static final String INCORRECT_SEASON = "null";

    private static final String TEST_GROUP_ID = "0000";

    private static final String TEST_GROUP_NAME = "Test";

    @Test(expected = UnknownValueException.class)
    public void testArgumentChecks1() throws UnknownValueException {
        getCachedSchedule(TEST_GROUP_ID, INCORRECT_SEASON);
    }

    @Test(expected = UnknownValueException.class)
    public void testArgumentChecks2() throws UnknownValueException {
        updateDateRanges(INCORRECT_SEASON);
    }

    @Test
    public void testCachedSchedule() throws UnknownValueException {
        assertNull(getCachedSchedule(INCORRECT_GROUP_ID, SEASON_AUTUMN));
        assertNull(getCachedSchedule(INCORRECT_GROUP_ID, SEASON_SPRING));
    }

    @Test
    public void testExistentGroupId() throws UnknownValueException {
        String groupName = getGroupName(TEST_GROUP_ID);
        assertEquals(groupName, TEST_GROUP_NAME);
    }

    @Test(expected = UnknownValueException.class)
    public void testNonExistentGroupId() throws UnknownValueException {
        getGroupName(INCORRECT_GROUP_ID);
    }

}
