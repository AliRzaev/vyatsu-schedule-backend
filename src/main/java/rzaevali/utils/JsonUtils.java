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

    public static final Gson STANDARD_JSON = new GsonBuilder().create();

    public static final Gson PRETTY_JSON = new GsonBuilder().setPrettyPrinting().create();

    public static String errorMessage(String message) {
        checkNotNull(message);

        return STANDARD_JSON.toJson(new ErrorMessage(message));
    }

}
