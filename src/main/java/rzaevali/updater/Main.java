package rzaevali.updater;

import rzaevali.utils.DBUtils;

public class Main {
    public static void main(String[] args) {
       DBUtils.updateDateRanges(DBUtils.SEASON_AUTUMN);
       DBUtils.updateDateRanges(DBUtils.SEASON_SPRING);
    }
}
