package rzaevali.api;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import rzaevali.exceptions.VyatsuScheduleException;
import rzaevali.utils.JsonUtils;
import rzaevali.utils.ScheduleUtilsKt;

import javax.servlet.ServletContext;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.FileInputStream;
import java.io.FileNotFoundException;

import static rzaevali.utils.JsonUtils.error;

@Path("vyatsu")
public class VyatSUv1 {

    private static final Logger logger = LogManager.getLogger("vyatsu");

    @Context
    private ServletContext context;

    @GET
    @Path("/calls")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getCalls() throws FileNotFoundException {
        logger.info("/calls");

        String path = context.getRealPath("/data/calls.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups.json")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getGroupsJSON() throws FileNotFoundException {
        logger.info("/groups.json");

        String path = context.getRealPath("/data/groups.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups.xml")
    @Produces(MediaType.APPLICATION_XML)
    public Response getGroupsXML() throws FileNotFoundException {
        logger.info("/groups.xml");

        String path = context.getRealPath("/data/groups.xml");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups/by_faculty.json")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getGroupsByFacultyJSON() throws FileNotFoundException {
        logger.info("/groups/by_faculty.json");

        String path = context.getRealPath("/data/faculties.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups/by_faculty.xml")
    @Produces(MediaType.APPLICATION_XML)
    public Response getGroupsByFacultyXML() throws FileNotFoundException {
        logger.info("/groups/by_faculty.xml");

        String path = context.getRealPath("/data/faculties.xml");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/schedule/{group_id}/{season}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getSchedule(
            @PathParam("group_id") String groupId,
            @PathParam("season") String season
    ) {
        try {
            logger.info("/schedule/{}/{}", groupId, season);

            String schedule = JsonUtils.getDefaultJson().toJson(ScheduleUtilsKt.getSchedule(groupId, season));
            return Response.ok(schedule).encoding("utf-8").build();
        } catch (VyatsuScheduleException e) {
            logger.error(e.getMessage());

            return Response.status(422)
                    .entity(error(e.getMessage()))
                    .build();
        } catch (Exception e) {
            logger.throwing(e);

            return Response.status(500)
                    .entity(error("Internal server error"))
                    .build();
        }
    }

}
