package rzaevali;

import javax.ws.rs.core.Application;
import javax.ws.rs.core.Response;

import org.glassfish.jersey.jaxb.internal.XmlJaxbElementProvider;
import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.test.JerseyTest;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class VyatSUTest extends JerseyTest {

    @Override
    protected Application configure() {
        return new ResourceConfig(VyatSU.class);
    }

    @Test
    public void testSchedule() {
        String output = target("/vyatsu/schedule/7777/autumn").request().get().readEntity(String.class);
        assertEquals("Expected 7777autumn", "7777autumn", output);
    }
}
