package rzaevali.utils;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.List;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

public class JsonUtils {

    private static class ErrorMessage {

        private String error;

        ErrorMessage(String message) {
            this.error = message;
        }

    }

    private static class Schedule {

        private List<List<List<String>>> weeks;

        private String group;

        private List<String> date_range;

        Schedule(List<List<List<String>>> weeks, String group, List<String> date_range) {
            this.weeks = weeks;
            this.group = group;
            this.date_range = date_range;
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

    public static String error(String message) {
        checkNotNull(message);

        return getDefaultJson().toJson(new ErrorMessage(message));
    }

    public static String schedule(ScheduleUtils.Schedule schedule) {
        return schedule(
                schedule.getWeeks(),
                schedule.getGroup(),
                schedule.getDateRange()
        );
    }

    public static String schedule(List<List<List<String>>> weeks, String group, List<String> date_range) {
        checkNotNull(weeks);
        checkNotNull(group);
        checkNotNull(date_range);
        checkArgument(date_range.size() == 2);

        return getDefaultJson().toJson(new Schedule(weeks, group, date_range));
    }
}
