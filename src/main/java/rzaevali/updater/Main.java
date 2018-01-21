package rzaevali.updater;

import rzaevali.exceptions.UnknownValueException;
import rzaevali.utils.DBUtils;
import rzaevali.utils.DateUtils;

import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.ZoneId;

public class Main {

    public static void main(String[] args) throws UnknownValueException {
        LocalDate currentDate = LocalDate.now(ZoneId.of("Europe/Moscow"));
        DayOfWeek currentDay = currentDate.getDayOfWeek();

        if (!currentDay.equals(DayOfWeek.SATURDAY)) {
            return;
        }

        if (DateUtils.isAutumn(currentDate)) {
            DBUtils.getInstance().updateDateRanges(DBUtils.SEASON_AUTUMN);
        }
        if (DateUtils.isSpring(currentDate)) {
            DBUtils.getInstance().updateDateRanges(DBUtils.SEASON_SPRING);
        }
    }

}
