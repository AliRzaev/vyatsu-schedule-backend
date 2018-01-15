package rzaevali.api;

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

    @Context
    private ServletContext context;

    @GET
    @Path("/calls")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getCallsV2() throws FileNotFoundException {
        String path = context.getRealPath("/data/calls-v2.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups.json")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getGroupsV2JSON() throws FileNotFoundException {
        String path = context.getRealPath("/data/groups-v2.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

}
