package rzaevali.utils;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class JsonUtils {

    public static final Gson STANDARD_JSON = new GsonBuilder().create();

    public static final Gson PRETTY_JSON = new GsonBuilder().setPrettyPrinting().create();

}
