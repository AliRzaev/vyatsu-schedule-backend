package rzaevali.utils;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import static com.google.common.base.Preconditions.checkNotNull;

public class JsonUtils {

    private static class ErrorMessage {

        private String error;

        ErrorMessage(String message) {
            this.error = message;
        }

    }

    private static final Gson STANDARD_JSON = new GsonBuilder().create();

    private static final Gson PRETTY_JSON = new GsonBuilder().setPrettyPrinting().create();

    public static Gson getDefaultJson() {
        if (System.getenv("DEBUG") != null) {
            return STANDARD_JSON;
        } else {
            return PRETTY_JSON;
        }
    }

    public static String errorMessage(String message) {
        checkNotNull(message);

        return getDefaultJson().toJson(new ErrorMessage(message));
    }

}
