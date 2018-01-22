package rzaevali;

import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.test.JerseyTest;
import org.junit.Test;
import rzaevali.api.VyatSUv1;

import javax.ws.rs.core.Application;
import javax.ws.rs.core.Response;

import static org.junit.Assert.assertEquals;

public class VyatSUv1Test extends JerseyTest {

    private static final String INCORRECT_GROUP_ID = "null";

    private static final String INCORRECT_SEASON = "null";

    private static final String TEST_GROUP_ID = "0000";

    @Override
    protected Application configure() {
        return new ResourceConfig(VyatSUv1.class);
    }

    @Test
    public void testIncorrectGroupId() {
        Response response = target(String.format("/vyatsu/schedule/%s/autumn", INCORRECT_GROUP_ID))
                .request()
                .get();
        assertEquals(response.getStatus(), 422);
    }

    @Test
    public void testIncorrectSeason() {
        Response response = target(String.format("/vyatsu/schedule/0000/%s", INCORRECT_SEASON))
                .request()
                .get();
        assertEquals(response.getStatus(), 422);
    }

    @Test
    public void testNonExistentScheduleAutumn() {
        Response response = target(String.format("/vyatsu/schedule/%s/autumn", TEST_GROUP_ID))
                .request()
                .get();
        assertEquals(response.getStatus(), 422);
    }

    @Test
    public void testNonExistentScheduleSpring() {
        Response response = target(String.format("/vyatsu/schedule/%s/spring", TEST_GROUP_ID))
                .request()
                .get();
        assertEquals(response.getStatus(), 422);
    }

}