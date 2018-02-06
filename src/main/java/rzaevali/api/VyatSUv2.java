package rzaevali.api;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.servlet.ServletContext;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.FileInputStream;
import java.io.FileNotFoundException;

@Path("vyatsu/v2")
public class VyatSUv2 {

    private static final Logger logger = LogManager.getLogger("vyatsu/v2");

    @Context
    private ServletContext context;

    @GET
    @Path("/calls")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getCallsV2() throws FileNotFoundException {
        logger.info("/calls");

        String path = context.getRealPath("/data/calls-v2.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups.json")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getGroupsV2JSON() throws FileNotFoundException {
        logger.info("/groups.json");

        String path = context.getRealPath("/data/groups-v2.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

}
