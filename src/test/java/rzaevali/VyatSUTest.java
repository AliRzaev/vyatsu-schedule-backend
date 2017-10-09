package rzaevali;

import javax.ws.rs.core.Application;

import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.test.JerseyTest;
import org.junit.Test;
import rzaevali.utils.PDFUtils;

import java.io.IOException;

import static org.junit.Assert.assertEquals;

public class VyatSUTest extends JerseyTest {

    @Override
    protected Application configure() {
        return new ResourceConfig(VyatSU.class);
    }

}
