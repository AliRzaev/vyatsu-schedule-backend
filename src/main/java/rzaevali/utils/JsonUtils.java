package rzaevali.utils;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.List;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public class JsonUtils {

    private static final Gson STANDARD_JSON = new GsonBuilder().create();

    private static final Gson PRETTY_JSON = new GsonBuilder().setPrettyPrinting().create();

    public static Gson getDefaultJson() {
        if (System.getenv("DEBUG") != null) {
            return STANDARD_JSON;
        } else {
            return PRETTY_JSON;
        }
    }
}
