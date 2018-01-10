package rzaevali.updater;

import rzaevali.exceptions.DocNotFoundException;
import rzaevali.utils.DBUtils;

public class Main {
    public static void main(String[] args) throws DocNotFoundException {
       DBUtils.updateDateRanges(DBUtils.SEASON_AUTUMN);
       DBUtils.updateDateRanges(DBUtils.SEASON_SPRING);
    }
}
