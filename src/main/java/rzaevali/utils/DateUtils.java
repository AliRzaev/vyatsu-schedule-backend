package rzaevali.utils;

import java.time.LocalDate;
import java.time.Month;

public class DateUtils {

    public static boolean isAutumn(LocalDate currentDate) {
        int monthValue = currentDate.getMonthValue();
        int augustValue = Month.AUGUST.getValue();
        int decemberValue = Month.DECEMBER.getValue();

        return monthValue <= decemberValue || monthValue >= augustValue;
    }

    public static boolean isSpring(LocalDate currentDate) {
        return !isAutumn(currentDate);
    }

}
