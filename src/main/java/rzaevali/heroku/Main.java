package rzaevali.heroku;

import rzaevali.routes.VyatSUv1;
import rzaevali.routes.VyatSUv2;

import static spark.Spark.port;

public class Main {

    public static void main(String[] args) throws Exception {
        String webPort = System.getenv("PORT");
        if (webPort == null || webPort.isEmpty()) {
            webPort = "8080";
        }

        port(Integer.parseInt(webPort));
        VyatSUv1.setRoutes();
        VyatSUv2.setRoutes();
    }
}
