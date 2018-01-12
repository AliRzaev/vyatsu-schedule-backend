package rzaevali;

import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.test.JerseyTest;
import org.junit.Test;

import javax.ws.rs.core.Application;
import javax.ws.rs.core.Response;

import static org.junit.Assert.assertEquals;

public class VyatSUTest extends JerseyTest {

    @Override
    protected Application configure() {
        return new ResourceConfig(VyatSU.class);
    }

    @Test
    public void testIncorrectGroupId() {
        Response response = target("/vyatsu/schedule/null/autumn")
                .request()
                .get();
        assertEquals(response.getStatus(), 422);
    }

    @Test
    public void testIncorrectSeason() {
        Response response = target("/vyatsu/schedule/0000/null")
                .request()
                .get();
        assertEquals(response.getStatus(), 422);
    }

    @Test
    public void testNonExistentScheduleAutumn() {
        Response response = target("/vyatsu/schedule/0000/autumn")
                .request()
                .get();
        assertEquals(response.getStatus(), 422);
    }

    @Test
    public void testNonExistentScheduleSpring() {
        Response response = target("/vyatsu/schedule/0000/spring")
                .request()
                .get();
        assertEquals(response.getStatus(), 422);
    }

}
