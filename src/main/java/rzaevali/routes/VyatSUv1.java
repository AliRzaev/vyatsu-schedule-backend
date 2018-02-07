package rzaevali.routes;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import rzaevali.exceptions.VyatsuScheduleException;
import rzaevali.utils.JsonUtils;
import rzaevali.utils.ScheduleUtilsKt;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;

import static rzaevali.utils.JsonUtils.error;
import static spark.Spark.get;
import static spark.Spark.path;

public class VyatSUv1 {

    private static final Logger logger = LogManager.getLogger("vyatsu");

    private static String readText(String path) throws IOException {
        return Files
                .readAllLines(Paths.get(path))
                .stream()
                .collect(Collectors.joining("\n"));
    }

    public static void setRoutes() {
        path("/vyatsu", () -> {
            get("/calls", (req, res) -> {
                logger.info("/calls");

                res.type("application/json");
                return readText("src/main/webapp/data/calls.json");
            });

            get("/groups.json", (req, res) -> {
                logger.info("/groups.json");

                res.type("application/json");
                return readText("src/main/webapp/data/groups.json");
            });

            get("/groups.xml", (req, res) -> {
                logger.info("/groups.xml");

                res.type("application/xml");
                return readText("src/main/webapp/data/groups.xml");
            });

            get("/groups/by_faculty.json", (req, res) -> {
                logger.info("/groups/by_faculty.json");

                res.type("application/json");
                return readText("src/main/webapp/data/faculties.json");
            });

            get("/groups/by_faculty.xml", (req, res) -> {
                logger.info("/groups/by_faculty.xml");

                res.type("application/xml");
                return readText("src/main/webapp/data/faculties.xml");
            });

            get("/schedule/:group_id/:season", (req, res) -> {
                String groupId = req.params("group_id");
                String season = req.params("season");
                res.type("application/json");
                try {
                    logger.info("/schedule/{}/{}", groupId, season);

                    return JsonUtils.getDefaultJson().toJson(ScheduleUtilsKt.getSchedule(groupId, season));
                } catch (VyatsuScheduleException e) {
                    logger.error("/schedule/{}/{}: {}", groupId, season, e.getMessage());

                    res.status(422);
                    return error(e.getMessage());
                } catch (Exception e) {
                    logger.error("/schedule/{}/{}", groupId, season);
                    logger.throwing(e);

                    res.status(500);
                    return error(e.getMessage());
                }
            });
        });
    }

}
