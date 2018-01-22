package rzaevali.utils;

import rzaevali.exceptions.UnknownValueException;
import rzaevali.exceptions.VyatsuScheduleException;

import java.util.List;
import java.util.Objects;

import static com.google.common.base.Preconditions.checkNotNull;
import static rzaevali.utils.DBUtils.ScheduleInfo;
import static rzaevali.utils.DBUtils.getSeasonKey;
import static rzaevali.utils.DateUtils.compareDates;

public class ScheduleUtils {

    private static final String BASE_URL = "https://www.vyatsu.ru/reports/schedule/Group/%s_%s_%s_%s.pdf";

    private static final boolean SCHEDULE_CACHE_ENABLED = Objects.equals(System.getenv("SCHEDULE_CACHE"), "enabled");

    public static String getSchedule(String groupId, String season) throws VyatsuScheduleException {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");

        if (SCHEDULE_CACHE_ENABLED) {
            return getScheduleUsingCache(groupId, season);
        } else {
            return getScheduleFromSite(groupId, season);
        }
    }

    private static String getScheduleFromSite(String groupId, String season) throws VyatsuScheduleException {
        List<String> range = DBUtils.getInstance().getDateRange(groupId, season);
        String group = DBUtils.getInstance().getGroupName(groupId);
        String url = buildUrl(groupId, season, range);

        return JsonUtils.schedule(
                PdfUtils.extractSchedule(url),
                group,
                range
        );
    }

    private static String getScheduleUsingCache(String groupId, String season) throws VyatsuScheduleException {
        List<String> range = DBUtils.getInstance().getDateRange(groupId, season);
        String group = DBUtils.getInstance().getGroupName(groupId);
        String url = buildUrl(groupId, season, range);
        ScheduleInfo cachedSchedule = DBUtils.getInstance().getCachedSchedule(groupId, season);

        if (cachedSchedule == null || compareDates(range, cachedSchedule.getDateRange()) > 0) {
            List<List<List<String>>> weeks = PdfUtils.extractSchedule(url);
            DBUtils.getInstance().updateSchedule(new ScheduleInfo(
                    weeks,
                    groupId,
                    range,
                    season
            ));

            return JsonUtils.schedule(
                    weeks,
                    group,
                    range
            );
        } else {
            return JsonUtils.schedule(
                    cachedSchedule.getWeeks(),
                    group,
                    range
            );
        }
    }

    private static String buildUrl(String groupId, String season, List<String> range) throws UnknownValueException {
        return String.format(
                BASE_URL,
                groupId,
                getSeasonKey(season),
                range.get(0),
                range.get(1)
        );
    }

}
