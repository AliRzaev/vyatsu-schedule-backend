package rzaevali;

import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.test.JerseyTest;

import javax.ws.rs.core.Application;

public class VyatSUTest extends JerseyTest {

    @Override
    protected Application configure() {
        return new ResourceConfig(VyatSU.class);
    }

}
