package rzaevali.updater;

import rzaevali.exceptions.UnknownValueException;
import rzaevali.utils.DateUtils;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.ZoneId;

import static rzaevali.utils.DBUtilsKt.*;

public class Main {

    public static void main(String[] args) throws UnknownValueException {
        LocalDate currentDate = LocalDate.now(ZoneId.of("Europe/Moscow"));
        DayOfWeek currentDay = currentDate.getDayOfWeek();

        if (!currentDay.equals(DayOfWeek.SATURDAY)) {
            return;
        }

        if (DateUtils.isAutumn(currentDate)) {
            updateDateRanges(SEASON_AUTUMN);
        }
        if (DateUtils.isSpring(currentDate)) {
            updateDateRanges(SEASON_SPRING);
        }
    }

}
