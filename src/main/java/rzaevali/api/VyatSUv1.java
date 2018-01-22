package rzaevali.api;

import rzaevali.exceptions.VyatsuScheduleException;
import rzaevali.utils.ScheduleUtils;

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

    @Context
    private ServletContext context;

    @GET
    @Path("/calls")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getCalls() throws FileNotFoundException {
        String path = context.getRealPath("/data/calls.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups.json")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getGroupsJSON() throws FileNotFoundException {
        String path = context.getRealPath("/data/groups.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups.xml")
    @Produces(MediaType.APPLICATION_XML)
    public Response getGroupsXML() throws FileNotFoundException {
        String path = context.getRealPath("/data/groups.xml");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups/by_faculty.json")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getGroupsByFacultyJSON() throws FileNotFoundException {
        String path = context.getRealPath("/data/faculties.json");
        return Response.ok().entity(new FileInputStream(path)).build();
    }

    @GET
    @Path("/groups/by_faculty.xml")
    @Produces(MediaType.APPLICATION_XML)
    public Response getGroupsByFacultyXML() throws FileNotFoundException {
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
            String schedule = ScheduleUtils.getSchedule(groupId, season);
            return Response.ok(schedule).encoding("utf-8").build();
        } catch (VyatsuScheduleException e) {
            return Response.status(422)
                    .entity(error(e.getMessage()))
                    .build();
        } catch (Exception e) {
            e.printStackTrace();

            return Response.status(500)
                    .entity(error("Internal server error"))
                    .build();
        }
    }

}