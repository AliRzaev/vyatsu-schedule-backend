package rzaevali.routes;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;

import static spark.Spark.get;
import static spark.Spark.path;

public class VyatSUv2 {

    private static final Logger logger = LogManager.getLogger("vyatsu/v2");

    private static String readText(String path) throws IOException {
        return Files
                .readAllLines(Paths.get(path))
                .stream()
                .collect(Collectors.joining("\n"));
    }

    public static void setRoutes() {
        path("/vyatsu/v2", () -> {
            get("/calls", (req, res) -> {
                logger.info("/calls");

                res.type("application/json");
                return readText("src/main/webapp/data/calls-v2.json");
            });

            get("/groups.json", (req, res) -> {
                logger.info("/groups.json");

                res.type("application/json");
                return readText("src/main/webapp/data/groups-v2.json");
            });
        });
    }

}
