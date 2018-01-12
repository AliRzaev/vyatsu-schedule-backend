package rzaevali.updater;

import rzaevali.exceptions.UnknownValueException;
import rzaevali.utils.DBUtils;

public class Main {
    public static void main(String[] args) throws UnknownValueException {
       DBUtils.getInstance().updateDateRanges(DBUtils.SEASON_AUTUMN);
       DBUtils.getInstance().updateDateRanges(DBUtils.SEASON_SPRING);
    }
}
