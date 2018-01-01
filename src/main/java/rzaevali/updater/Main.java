package rzaevali.updater;

import rzaevali.utils.DBUtils;

public class Main {
    public static void main(String[] args) {
       DBUtils.updateDateRanges("autumn");
       DBUtils.updateDateRanges("spring");
    }
}
