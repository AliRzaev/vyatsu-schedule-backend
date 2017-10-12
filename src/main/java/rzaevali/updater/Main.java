package rzaevali.updater;

import rzaevali.utils.DBUtils;

public class Main {
    public static void main(String[] args) throws Exception {
//        DBUtils.updateDateRanges("autumn");
        System.out.println(DBUtils.getDateRange("7794", "autumn").toString());
    }
}
