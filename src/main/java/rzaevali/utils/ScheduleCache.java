package rzaevali.utils;

import rzaevali.utils.ScheduleUtils.Schedule;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

import static com.google.common.base.Preconditions.checkNotNull;

public class ScheduleCache {
    private static class Pair {
        private String first;
        private String second;

        Pair(String first, String second) {
            this.first = first;
            this.second = second;
        }

        @Override
        public String toString() {
            return String.format("Pair[%s, %s]", first, second);
        }

        @Override
        public int hashCode() {
            return first.hashCode() ^ second.hashCode();
        }

        @Override
        public boolean equals(Object other) {
            if (other instanceof Pair) {
                Pair pair = (Pair)other;
                return Objects.equals(first, pair.first) && Objects.equals(second, pair.second);
            } else {
                return false;
            }
        }
    }

    private static ScheduleCache ourInstance = new ScheduleCache();

    public static ScheduleCache getInstance() {
        return ourInstance;
    }

    private static final Map<Pair, Schedule> cache = new HashMap<>();

    public Schedule getSchedule(String groupId, String season) {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");

        return cache.get(new Pair(groupId, season));
    }

    public void updateSchedule(String groupId, String season, Schedule schedule) {
        checkNotNull(groupId, "groupId must not be null");
        checkNotNull(season, "season must not be null");
        checkNotNull(schedule, "schedule object must not be null");

        cache.put(new Pair(groupId, season), schedule);
    }

    public void clearCache() {
        cache.clear();
    }

    private ScheduleCache() {
    }
}
