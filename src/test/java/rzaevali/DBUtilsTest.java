package rzaevali;

import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.test.JerseyTest;
import rzaevali.utils.DBUtils;

import javax.ws.rs.core.Application;

public class DBUtilsTest extends JerseyTest {

    @Override
    protected Application configure() {
        return new ResourceConfig(DBUtils.class);
    }

}
